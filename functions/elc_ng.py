from dataclasses import dataclass, field
import struct
import typing

import usb


@dataclass
class Response:
    @classmethod
    def from_bytes(cls, data):
        return cls(data)


@dataclass
class RawResponse(Response):
    raw: bytes


@dataclass
class Command:
    opcode: typing.ClassVar[int] = None
    response_class: typing.ClassVar[Response] = RawResponse

    def header(self):
        return bytes((0x03, self.opcode))

    def payload(self):
        return self.header()

    def as_bytes(self):
        return self.payload().ljust(33, b'\x00')


@dataclass
class CommandWithSubcommand(Command):
    subcommands: typing.ClassVar[dict] = None

    subcommand: str

    def __post_init__(self):
        if(
            self.subcommand and
            self.subcommand not in self.subcommands
        ):
            raise AttributeError(
                f'Invalid subcommand for {type(self).__name__}.'
                f'Valid choices are: {", ".join(self.subcommands)}.'
            )

    def payload(self):
        return super().payload() + bytes([self.subcommands[self.subcommand]])


@dataclass
class VersionResponse(Response):
    version_info: tuple

    args_struct = struct.Struct('>BBB')

    @classmethod
    def from_bytes(cls, data):
        return cls(cls.args_struct.unpack(data[3:6]))


@dataclass
class PlatformResponse(Response):
    platform_id: int
    zone_count: int

    args_struct = struct.Struct('>HB')

    @classmethod
    def from_bytes(cls, data):
        return cls(*cls.args_struct.unpack(data[3:6]))


@dataclass
class AnimationCountResponse(Response):
    animation_count: int
    last_animation_id: int

    args_struct = struct.Struct('>HH')

    @classmethod
    def from_bytes(cls, data):
        return cls(*cls.args_struct.unpack(data[3:7]))


@dataclass
class QueryCommand(CommandWithSubcommand):
    opcode = 0x20
    # XXX: Some aren't implemented on hardware?
    subcommands = {
        'version': 0x00,
        # 'status': 0x01,
        'platform': 0x02,
        'animation_count': 0x03,
        # 'animation_by_id': 0x04,
        # 'series': 0x05,
    }
    response_classes = {
        'version': VersionResponse,
        'platform': PlatformResponse,
        'animation_count': AnimationCountResponse,
    }

    def __post_init__(self):
        super().__post_init__()
        self.response_class = self.response_classes.get(
            self.subcommand,
            Response
        )


@dataclass
class AnimationCommand(CommandWithSubcommand):
    subcommands = {
        'start_new': 0x01,
        'finish_save': 0x02,
        'finish_play': 0x03,
        'remove': 0x04,
        'play': 0x05,
        'set_default': 0x06,
        'set_startup': 0x07,
    }

    animation_id: int

    args_struct = struct.Struct('>HH')

    def __post_init__(self):
        super().__post_init__()
        self.opcode = (
            0x21 if self.is_power_animation else 0x22
        )

    @property
    def is_power_animation(self):
        return 0x5b <= self.animation_id <= 0x60

    def payload(self):
        return self.header() + self.args_struct.pack(
            self.subcommands[self.subcommand],
            self.animation_id
        )


@dataclass
class StartSeriesCommand(Command):
    opcode = 0x23

    zones: typing.Collection[int]
    loop: bool = 1

    args_struct = struct.Struct('>BH')

    def payload(self):
        zones = self.zones
        return (
            super().payload()
            + self.args_struct.pack(self.loop, len(zones))
            + bytes(zones)
        )


@dataclass
class Action:
    effect: str
    red: int
    green: int
    blue: int
    duration: int = 1000
    tempo: int = 60

    effects: typing.ClassVar[dict] = {
        'color': 0x00,
        'pulse': 0x01,
        'morph': 0x02,
    }

    args_struct = struct.Struct('>BHHBBB')

    def __post_init__(self):
        if self.effect not in self.effects:
            raise AttributeError(
                'Invalid effect. '
                f'Possible choices are: {", ".join(self.effects)}'
            )

    def as_bytes(self):
        return self.args_struct.pack(
            self.effects[self.effect],
            self.duration,
            self.tempo,
            self.red,
            self.green,
            self.blue,
        )


@dataclass
class AddActionsCommand(Command):
    opcode = 0x24

    actions: typing.Collection[Action]

    def __post_init__(self):
        if len(self.actions) > 3:
            raise AttributeError("Can't add more than 3 actions at a time.")

    def payload(self):
        return super().payload() + b''.join(
            action.as_bytes() for action in self.actions
        )


@dataclass
class DimCommand(Command):
    opcode = 0x26

    zones: typing.Collection[int]
    level: int

    args_struct = struct.Struct('>BH')

    def payload(self):
        zones = self.zones
        return (
            super().payload()
            + self.args_struct.pack(self.level, len(zones))
            + bytes(zones)
        )


@dataclass
class ColorCommand(Command):
    opcode = 0x27

    zones: typing.Collection[int]
    red: int
    green: int
    blue: int

    args_struct = struct.Struct('>BBBH')

    def payload(self):
        zones = self.zones
        return (
            super().payload()
            + self.args_struct.pack(
                self.red,
                self.green,
                self.blue,
                len(zones),
            ) + bytes(zones)
        )


@dataclass
class ELC:
    vid: int
    pid: int

    usb_device: usb.core.Device = field(init=False, compare=False)
    attached: bool = field(default=False, init=False, compare=False)

    def __post_init__(self):
        vid, pid = self.vid, self.pid

        results = list(usb.core.find(
            idVendor=vid,
            idProduct=pid,
            find_all=True,
        ))

        if not results:
            raise AttributeError(
                f'USB device with VID:PID {vid}:{pid} not found.'
            )

        if len(results) > 1:
            raise AttributeError(
                f'More than one USB device with VID:PID {vid}:{pid} was found.'
            )

        self.usb_device = results[0]

    def __enter__(self):
        self._attach()
        return self

    def __exit__(self, *args):
        self._detach()

    def _attach(self):
        device = self.usb_device

        if device.is_kernel_driver_active(0):
            device.detach_kernel_driver(0)

        default_configuration = device.configurations()[0]
        current_configuration = None

        try:
            current_configuration = device.get_active_configuration()
        except usb.USBError:
            # No active configuration
            pass

        if(
            not current_configuration
            or current_configuration.bConfigurationValue
            != default_configuration.bConfigurationValue
        ):
            device.set_configuration()

        self.attached = True

    def _detach(self):
        device = self.usb_device

        if not device.is_kernel_driver_active(0):
            usb.util.release_interface(device, 0)
            device.attach_kernel_driver(0)

        self.attached = False

    def execute(self, command: Command) -> Response:
        if not self.attached:
            raise ValueError(
                "ELC isn't currently attached to any USB device. "
                'Please use execute() inside a "with your_elc:" block.'
            )

        self.usb_send(command.as_bytes())
        return command.response_class.from_bytes(self.usb_recv())

    def usb_send(self, data):
        self.usb_device.ctrl_transfer(
            usb.TYPE_CLASS | usb.RECIP_INTERFACE | usb.ENDPOINT_OUT,
            usb.REQ_SET_CONFIGURATION,
            0x202,
            0,
            data
        )

    def usb_recv(self):
        return self.usb_device.ctrl_transfer(
            usb.TYPE_CLASS | usb.RECIP_INTERFACE | usb.ENDPOINT_IN,
            usb.REQ_CLEAR_FEATURE,
            0x101,
            0,
            33  # Expected length of response
        )