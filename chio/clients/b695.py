
from typing import Iterable, Tuple
from .b659 import b659
from ..constants import *
from ..types import *
from ..io import *

class b695(b659):
    """
    b695 changes the rank datatype from u16 to s32.
    """
    version = 695

    @classmethod
    def write_user_stats(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        write_u32(stream, info.id)
        write_u8(stream, Completeness.Statistics)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u32(stream, info.stats.rank)
        yield PacketType.BanchoUserStats, stream.data

    @classmethod
    def write_user_presence(cls, info: UserInfo) -> Iterable[Tuple[PacketType, bytes]]:
        stream = MemoryStream()

        if info.presence.is_irc:
            yield next(cls.write_irc_join(info.name))
            return

        write_u32(stream, info.id)
        write_u8(stream, Completeness.Full)
        stream.write(cls.write_status_update(info.status))
        write_u64(stream, info.stats.rscore)
        write_f32(stream, info.stats.accuracy)
        write_u32(stream, info.stats.playcount)
        write_u64(stream, info.stats.tscore)
        write_u32(stream, info.stats.rank)
        write_string(stream, info.name)
        write_string(stream, info.avatar_filename)
        write_u8(stream, info.presence.timezone+24)
        write_string(stream, info.presence.country_string)
        write_u8(stream, info.presence.permissions)
        yield PacketType.BanchoUserStats, stream.data
