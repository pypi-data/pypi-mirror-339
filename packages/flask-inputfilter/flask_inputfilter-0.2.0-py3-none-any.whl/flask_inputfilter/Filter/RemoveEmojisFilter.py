import re
import warnings
from typing import Any, Optional, Union

from flask_inputfilter.Filter import BaseFilter

emoji_pattern = (
    r"["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+"
)


class RemoveEmojisFilter(BaseFilter):
    """
    Filter that removes emojis from a string.
    """

    def apply(self, value: Any) -> Union[Optional[str], Any]:
        warnings.warn(
            "RemoveEmojisFilter is deprecated and will be discontinued. "
            "It can safely be replaced with StringRemoveEmojisFilter.",
            DeprecationWarning,
        )

        if not isinstance(value, str):
            return value

        return re.sub(emoji_pattern, "", value)
