from .b388 import b388
from ..constants import *
from ..types import *
from ..io import *

class b402(b388):
    """
    b402 adds support for changing host players inside multiplayer matches.
    """
    version = 402

    @classmethod
    def read_match_transfer_host(cls, stream: MemoryStream) -> int:
        return read_s32(stream)

    @classmethod
    def write_match(cls, match: Match) -> bytes:
        stream = MemoryStream()
        write_u8(stream, match.id)
        write_boolean(stream, match.in_progress)
        write_u8(stream, match.type)
        write_u16(stream, match.mods.value)
        write_string(stream, match.name)
        write_string(stream, match.beatmap_text)
        write_s32(stream, match.beatmap_id)
        write_string(stream, match.beatmap_checksum)

        for slot in match.slots:
            write_u8(stream, slot.status.value)

        for slot in match.slots:
            if slot.has_player:
                write_s32(stream, slot.user_id)

        write_s32(stream, match.host_id)
        return stream.data

    @classmethod
    def read_match(cls, stream: MemoryStream) -> Match:
        match = Match()
        match.id = read_u8(stream)
        match.in_progress = read_boolean(stream)
        match.type = MatchType(read_u8(stream))
        match.mods = Mods(read_u16(stream))
        match.name = read_string(stream)
        match.beatmap_text = read_string(stream)
        match.beatmap_id = read_s32(stream)
        match.beatmap_checksum = read_string(stream)
        match.slots = [
            MatchSlot(status=SlotStatus(read_u8(stream)))
            for _ in range(cls.slot_size)
        ]

        for slot in match.slots:
            if slot.has_player:
                slot.user_id = read_s32(stream)

        match.host_id = read_s32(stream)
        return match
