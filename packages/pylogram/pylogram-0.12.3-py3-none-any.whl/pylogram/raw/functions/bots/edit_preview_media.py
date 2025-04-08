#  Pylogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2023 Dan <https://github.com/delivrance>
#  Copyright (C) 2023-2024 Pylakey <https://github.com/pylakey>
#
#  This file is part of Pylogram.
#
#  Pylogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pylogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pylogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pylogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pylogram.raw.core import TLObject
from pylogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class EditPreviewMedia(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``201``
        - ID: ``8525606F``

    Parameters:
        bot (:obj:`InputUser <pylogram.raw.base.InputUser>`):
            N/A

        lang_code (``str``):
            N/A

        media (:obj:`InputMedia <pylogram.raw.base.InputMedia>`):
            N/A

        new_media (:obj:`InputMedia <pylogram.raw.base.InputMedia>`):
            N/A

    Returns:
        :obj:`BotPreviewMedia <pylogram.raw.base.BotPreviewMedia>`
    """

    __slots__: List[str] = ["bot", "lang_code", "media", "new_media"]

    ID = 0x8525606f
    QUALNAME = "functions.bots.EditPreviewMedia"

    def __init__(self, *, bot: "raw.base.InputUser", lang_code: str, media: "raw.base.InputMedia", new_media: "raw.base.InputMedia") -> None:
        self.bot = bot  # InputUser
        self.lang_code = lang_code  # string
        self.media = media  # InputMedia
        self.new_media = new_media  # InputMedia

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EditPreviewMedia":
        # No flags
        
        bot = TLObject.read(b)
        
        lang_code = String.read(b)
        
        media = TLObject.read(b)
        
        new_media = TLObject.read(b)
        
        return EditPreviewMedia(bot=bot, lang_code=lang_code, media=media, new_media=new_media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.bot.write())
        
        b.write(String(self.lang_code))
        
        b.write(self.media.write())
        
        b.write(self.new_media.write())
        
        return b.getvalue()
