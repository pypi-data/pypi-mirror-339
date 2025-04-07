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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack111ll1l11_opy_ import get_logger
logger = get_logger(__name__)
bstack111llllll11_opy_: Dict[str, float] = {}
bstack111llll1ll1_opy_: List = []
bstack111llll1l1l_opy_ = 5
bstack1llll111l1_opy_ = os.path.join(os.getcwd(), bstack11l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࠬᱜ"), bstack11l1l11_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬᱝ"))
logging.getLogger(bstack11l1l11_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠬᱞ")).setLevel(logging.WARNING)
lock = FileLock(bstack1llll111l1_opy_+bstack11l1l11_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᱟ"))
class bstack111llll1l11_opy_:
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
    def __init__(self, duration: float, name: str, start_time: float, bstack111lllll1l1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111lllll1l1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11l1l11_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࠨᱠ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lll1llll1l_opy_:
    global bstack111llllll11_opy_
    @staticmethod
    def bstack1ll1ll1lll1_opy_(key: str):
        bstack1ll1ll1l1l1_opy_ = bstack1lll1llll1l_opy_.bstack1l1111lllll_opy_(key)
        bstack1lll1llll1l_opy_.mark(bstack1ll1ll1l1l1_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᱡ"))
        return bstack1ll1ll1l1l1_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111llllll11_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥᱢ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lll1llll1l_opy_.mark(end)
            bstack1lll1llll1l_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧᱣ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111llllll11_opy_ or end not in bstack111llllll11_opy_:
                logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠠࡰࡴࠣࡩࡳࡪࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠦᱤ").format(start,end))
                return
            duration: float = bstack111llllll11_opy_[end] - bstack111llllll11_opy_[start]
            bstack111lllll1ll_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨᱥ"), bstack11l1l11_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᱦ")).lower() == bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᱧ")
            bstack111llll1lll_opy_: bstack111llll1l11_opy_ = bstack111llll1l11_opy_(duration, label, bstack111llllll11_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11l1l11_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᱨ"), 0), command, test_name, hook_type, bstack111lllll1ll_opy_)
            del bstack111llllll11_opy_[start]
            del bstack111llllll11_opy_[end]
            bstack1lll1llll1l_opy_.bstack111lllll111_opy_(bstack111llll1lll_opy_)
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡥࡢࡵࡸࡶ࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥᱩ").format(e))
    @staticmethod
    def bstack111lllll111_opy_(bstack111llll1lll_opy_):
        os.makedirs(os.path.dirname(bstack1llll111l1_opy_)) if not os.path.exists(os.path.dirname(bstack1llll111l1_opy_)) else None
        bstack1lll1llll1l_opy_.bstack111llllll1l_opy_()
        try:
            with lock:
                with open(bstack1llll111l1_opy_, bstack11l1l11_opy_ (u"ࠣࡴ࠮ࠦᱪ"), encoding=bstack11l1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᱫ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111llll1lll_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111lllll11l_opy_:
            logger.debug(bstack11l1l11_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠤࢀࢃࠢᱬ").format(bstack111lllll11l_opy_))
            with lock:
                with open(bstack1llll111l1_opy_, bstack11l1l11_opy_ (u"ࠦࡼࠨᱭ"), encoding=bstack11l1l11_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᱮ")) as file:
                    data = [bstack111llll1lll_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡡࡱࡲࡨࡲࡩࠦࡻࡾࠤᱯ").format(str(e)))
        finally:
            if os.path.exists(bstack1llll111l1_opy_+bstack11l1l11_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨᱰ")):
                os.remove(bstack1llll111l1_opy_+bstack11l1l11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᱱ"))
    @staticmethod
    def bstack111llllll1l_opy_():
        attempt = 0
        while (attempt < bstack111llll1l1l_opy_):
            attempt += 1
            if os.path.exists(bstack1llll111l1_opy_+bstack11l1l11_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣᱲ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack1l1111lllll_opy_(label: str) -> str:
        try:
            return bstack11l1l11_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤᱳ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᱴ").format(e))