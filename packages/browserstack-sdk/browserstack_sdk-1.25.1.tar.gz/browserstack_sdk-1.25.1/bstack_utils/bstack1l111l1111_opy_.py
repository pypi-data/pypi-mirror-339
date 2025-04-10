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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack1l1ll1111l_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1llll1l_opy_: Dict[str, float] = {}
bstack111ll11111l_opy_: List = []
bstack111ll1111l1_opy_ = 5
bstack1l11l11ll_opy_ = os.path.join(os.getcwd(), bstack1ll1l1_opy_ (u"ࠫࡱࡵࡧࠨᳫ"), bstack1ll1l1_opy_ (u"ࠬࡱࡥࡺ࠯ࡰࡩࡹࡸࡩࡤࡵ࠱࡮ࡸࡵ࡮ࠨᳬ"))
logging.getLogger(bstack1ll1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡰࡴࡩ࡫ࠨ᳭")).setLevel(logging.WARNING)
lock = FileLock(bstack1l11l11ll_opy_+bstack1ll1l1_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨᳮ"))
class bstack111ll111111_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1llll11_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1llll11_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1ll1l1_opy_ (u"ࠣ࡯ࡨࡥࡸࡻࡲࡦࠤᳯ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll111l11l_opy_:
    global bstack111l1llll1l_opy_
    @staticmethod
    def bstack1ll1ll111ll_opy_(key: str):
        bstack1ll1l1l111l_opy_ = bstack1lll111l11l_opy_.bstack11llll111l1_opy_(key)
        bstack1lll111l11l_opy_.mark(bstack1ll1l1l111l_opy_+bstack1ll1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᳰ"))
        return bstack1ll1l1l111l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1llll1l_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᳱ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll111l11l_opy_.mark(end)
            bstack1lll111l11l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦ࡫ࡦࡻࠣࡱࡪࡺࡲࡪࡥࡶ࠾ࠥࢁࡽࠣᳲ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1llll1l_opy_ or end not in bstack111l1llll1l_opy_:
                logger.debug(bstack1ll1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡶࡤࡶࡹࠦ࡫ࡦࡻࠣࡻ࡮ࡺࡨࠡࡸࡤࡰࡺ࡫ࠠࡼࡿࠣࡳࡷࠦࡥ࡯ࡦࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠢᳳ").format(start,end))
                return
            duration: float = bstack111l1llll1l_opy_[end] - bstack111l1llll1l_opy_[start]
            bstack111ll1111ll_opy_ = os.environ.get(bstack1ll1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡉࡏࡃࡕ࡝ࡤࡏࡓࡠࡔࡘࡒࡓࡏࡎࡈࠤ᳴"), bstack1ll1l1_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨᳵ")).lower() == bstack1ll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᳶ")
            bstack111l1lll1ll_opy_: bstack111ll111111_opy_ = bstack111ll111111_opy_(duration, label, bstack111l1llll1l_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1ll1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠤ᳷"), 0), command, test_name, hook_type, bstack111ll1111ll_opy_)
            del bstack111l1llll1l_opy_[start]
            del bstack111l1llll1l_opy_[end]
            bstack1lll111l11l_opy_.bstack111l1llllll_opy_(bstack111l1lll1ll_opy_)
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡨࡥࡸࡻࡲࡪࡰࡪࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨ᳸").format(e))
    @staticmethod
    def bstack111l1llllll_opy_(bstack111l1lll1ll_opy_):
        os.makedirs(os.path.dirname(bstack1l11l11ll_opy_)) if not os.path.exists(os.path.dirname(bstack1l11l11ll_opy_)) else None
        bstack1lll111l11l_opy_.bstack111ll111l11_opy_()
        try:
            with lock:
                with open(bstack1l11l11ll_opy_, bstack1ll1l1_opy_ (u"ࠦࡷ࠱ࠢ᳹"), encoding=bstack1ll1l1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᳺ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1lll1ll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1lllll1_opy_:
            logger.debug(bstack1ll1l1_opy_ (u"ࠨࡆࡪ࡮ࡨࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠠࡼࡿࠥ᳻").format(bstack111l1lllll1_opy_))
            with lock:
                with open(bstack1l11l11ll_opy_, bstack1ll1l1_opy_ (u"ࠢࡸࠤ᳼"), encoding=bstack1ll1l1_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᳽")) as file:
                    data = [bstack111l1lll1ll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴࠢࡤࡴࡵ࡫࡮ࡥࠢࡾࢁࠧ᳾").format(str(e)))
        finally:
            if os.path.exists(bstack1l11l11ll_opy_+bstack1ll1l1_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤ᳿")):
                os.remove(bstack1l11l11ll_opy_+bstack1ll1l1_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᴀ"))
    @staticmethod
    def bstack111ll111l11_opy_():
        attempt = 0
        while (attempt < bstack111ll1111l1_opy_):
            attempt += 1
            if os.path.exists(bstack1l11l11ll_opy_+bstack1ll1l1_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᴁ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11llll111l1_opy_(label: str) -> str:
        try:
            return bstack1ll1l1_opy_ (u"ࠨࡻࡾ࠼ࡾࢁࠧᴂ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1ll1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥᴃ").format(e))