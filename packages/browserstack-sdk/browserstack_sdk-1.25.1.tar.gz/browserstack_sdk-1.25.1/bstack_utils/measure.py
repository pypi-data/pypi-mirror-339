# coding: UTF-8
import sys
bstack11l1ll1_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstack1l11111_opy_ = 7
def bstack1ll1l1_opy_ (bstack1l1ll1_opy_):
    global bstack1l111ll_opy_
    bstack1lll1ll_opy_ = ord (bstack1l1ll1_opy_ [-1])
    bstack111llll_opy_ = bstack1l1ll1_opy_ [:-1]
    bstack1l1l11l_opy_ = bstack1lll1ll_opy_ % len (bstack111llll_opy_)
    bstack1l1l1l_opy_ = bstack111llll_opy_ [:bstack1l1l11l_opy_] + bstack111llll_opy_ [bstack1l1l11l_opy_:]
    if bstack11l1ll1_opy_:
        bstack11ll111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    else:
        bstack11ll111_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstackl_opy_ + bstack1lll1ll_opy_) % bstack1l11111_opy_) for bstackl_opy_, char in enumerate (bstack1l1l1l_opy_)])
    return eval (bstack11ll111_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack1l1ll1111l_opy_ import get_logger
from bstack_utils.bstack1l111l1111_opy_ import bstack1lll111l11l_opy_
bstack1l111l1111_opy_ = bstack1lll111l11l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l1l111l1_opy_: Optional[str] = None):
    bstack1ll1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡊࡥࡤࡱࡵࡥࡹࡵࡲࠡࡶࡲࠤࡱࡵࡧࠡࡶ࡫ࡩࠥࡹࡴࡢࡴࡷࠤࡹ࡯࡭ࡦࠢࡲࡪࠥࡧࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠏࠦࠠࠡࠢࡤࡰࡴࡴࡧࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࠥࡴࡡ࡮ࡧࠣࡥࡳࡪࠠࡴࡶࡤ࡫ࡪ࠴ࠊࠡࠢࠣࠤࠧࠨࠢᰚ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1l1l111l_opy_: str = bstack1l111l1111_opy_.bstack11llll111l1_opy_(label)
            start_mark: str = label + bstack1ll1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᰛ")
            end_mark: str = label + bstack1ll1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᰜ")
            result = None
            try:
                if stage.value == STAGE.bstack1l11ll11_opy_.value:
                    bstack1l111l1111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l111l1111_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l1l111l1_opy_)
                elif stage.value == STAGE.bstack1llll1l1_opy_.value:
                    start_mark: str = bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᰝ")
                    end_mark: str = bstack1ll1l1l111l_opy_ + bstack1ll1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᰞ")
                    bstack1l111l1111_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l111l1111_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l1l111l1_opy_)
            except Exception as e:
                bstack1l111l1111_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l1l111l1_opy_)
            return result
        return wrapper
    return decorator