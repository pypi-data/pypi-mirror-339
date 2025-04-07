# coding: UTF-8
import sys
bstack11111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack111_opy_ = 7
def bstack11l1l11_opy_ (bstack11lll_opy_):
    global bstack1l11l11_opy_
    bstack1l1l1_opy_ = ord (bstack11lll_opy_ [-1])
    bstack1l111ll_opy_ = bstack11lll_opy_ [:-1]
    bstack11l_opy_ = bstack1l1l1_opy_ % len (bstack1l111ll_opy_)
    bstack11l111l_opy_ = bstack1l111ll_opy_ [:bstack11l_opy_] + bstack1l111ll_opy_ [bstack11l_opy_:]
    if bstack11111ll_opy_:
        bstack1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack1l_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1l1l11_opy_ + bstack1l1l1_opy_) % bstack111_opy_) for bstack1l1l11_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack1l_opy_)
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack111ll1l11_opy_ import get_logger
from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
bstack1l1ll1l11l_opy_ = bstack1lll1llll1l_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack11ll11ll11_opy_: Optional[str] = None):
    bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦᮋ")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1ll1l1l1_opy_: str = bstack1l1ll1l11l_opy_.bstack1l1111lllll_opy_(label)
            start_mark: str = label + bstack11l1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᮌ")
            end_mark: str = label + bstack11l1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᮍ")
            result = None
            try:
                if stage.value == STAGE.bstack1ll11l11ll_opy_.value:
                    bstack1l1ll1l11l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1l1ll1l11l_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack11ll11ll11_opy_)
                elif stage.value == STAGE.bstack1l1ll1lll_opy_.value:
                    start_mark: str = bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᮎ")
                    end_mark: str = bstack1ll1ll1l1l1_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᮏ")
                    bstack1l1ll1l11l_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1l1ll1l11l_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack11ll11ll11_opy_)
            except Exception as e:
                bstack1l1ll1l11l_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack11ll11ll11_opy_)
            return result
        return wrapper
    return decorator