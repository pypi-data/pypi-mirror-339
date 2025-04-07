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
import json
import subprocess
import threading
import time
import sys
import grpc
import os
from browserstack_sdk import sdk_pb2_grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111l1llll_opy_ import bstack1111l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11llll1_opy_ import bstack1lllll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lllll11l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll11l_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll11llll_opy_ import bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l111_opy_ import bstack1lll11111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1l1l_opy_ import bstack1lllll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1111l_opy_ import bstack1lll1ll1111_opy_
from browserstack_sdk.sdk_cli.bstack11l11ll11l_opy_ import bstack11l11ll11l_opy_, bstack1llll111ll_opy_, bstack111111ll1_opy_
from browserstack_sdk.sdk_cli.pytest_bdd_framework import PytestBDDFramework
from browserstack_sdk.sdk_cli.bstack1lllll11lll_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import bstack11111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1111l1_opy_ import bstack1llllll11ll_opy_
from bstack_utils.helper import Notset, bstack1llllll1l11_opy_, get_cli_dir, bstack1lll111ll1l_opy_, bstack1lll1ll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework
from bstack_utils.helper import Notset, bstack1llllll1l11_opy_, get_cli_dir, bstack1lll111ll1l_opy_, bstack1lll1ll11l_opy_, bstack111ll11ll_opy_, bstack1ll11l11l_opy_, bstack1l1l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llllll1lll_opy_, bstack1lllllll111_opy_, bstack1lll111lll1_opy_, bstack1lll11ll111_opy_
from browserstack_sdk.sdk_cli.bstack1111l11lll_opy_ import bstack11111l11ll_opy_, bstack1111l1ll1l_opy_, bstack111111111l_opy_
from bstack_utils.constants import *
from bstack_utils import bstack111ll1l11_opy_
from typing import Any, List, Union, Dict
import traceback
from google.protobuf.json_format import MessageToDict
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path
from functools import wraps
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1lll1l1lll_opy_, bstack1l1lll1l1_opy_
logger = bstack111ll1l11_opy_.get_logger(__name__, bstack111ll1l11_opy_.bstack1lll111ll11_opy_())
def bstack1lllll1l1l1_opy_(bs_config):
    bstack1llll11l1l1_opy_ = None
    bstack1llllll1111_opy_ = None
    try:
        bstack1llllll1111_opy_ = get_cli_dir()
        bstack1llll11l1l1_opy_ = bstack1lll111ll1l_opy_(bstack1llllll1111_opy_)
        bstack1llll1l1lll_opy_ = bstack1llllll1l11_opy_(bstack1llll11l1l1_opy_, bstack1llllll1111_opy_, bs_config)
        bstack1llll11l1l1_opy_ = bstack1llll1l1lll_opy_ if bstack1llll1l1lll_opy_ else bstack1llll11l1l1_opy_
        if not bstack1llll11l1l1_opy_:
            raise ValueError(bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡖࡈࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡑࡃࡗࡌࠧဣ"))
    except Exception as ex:
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡥࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫ࠥࡺࡨࡦࠢ࡯ࡥࡹ࡫ࡳࡵࠢࡥ࡭ࡳࡧࡲࡺࠢࡾࢁࠧဤ").format(ex))
        bstack1llll11l1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡇࡏࡎࡠࡒࡄࡘࡍࠨဥ"))
        if bstack1llll11l1l1_opy_:
            logger.debug(bstack11l1l11_opy_ (u"ࠦࡋࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭ࠣࡸࡴࠦࡓࡅࡍࡢࡇࡑࡏ࡟ࡃࡋࡑࡣࡕࡇࡔࡉࠢࡩࡶࡴࡳࠠࡦࡰࡹ࡭ࡷࡵ࡮࡮ࡧࡱࡸ࠿ࠦࠢဦ") + str(bstack1llll11l1l1_opy_) + bstack11l1l11_opy_ (u"ࠧࠨဧ"))
        else:
            logger.debug(bstack11l1l11_opy_ (u"ࠨࡎࡰࠢࡹࡥࡱ࡯ࡤࠡࡕࡇࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡐࡂࡖࡋࠤ࡫ࡵࡵ࡯ࡦࠣ࡭ࡳࠦࡥ࡯ࡸ࡬ࡶࡴࡴ࡭ࡦࡰࡷ࠿ࠥࡹࡥࡵࡷࡳࠤࡲࡧࡹࠡࡤࡨࠤ࡮ࡴࡣࡰ࡯ࡳࡰࡪࡺࡥ࠯ࠤဨ"))
    return bstack1llll11l1l1_opy_, bstack1llllll1111_opy_
bstack1lll11ll1ll_opy_ = bstack11l1l11_opy_ (u"ࠢ࠺࠻࠼࠽ࠧဩ")
bstack1lll1lll1l1_opy_ = bstack11l1l11_opy_ (u"ࠣࡴࡨࡥࡩࡿࠢဪ")
bstack1llll1l1ll1_opy_ = bstack11l1l11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨါ")
bstack1lll1ll1ll1_opy_ = bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡐࡎ࡙ࡔࡆࡐࡢࡅࡉࡊࡒࠣာ")
bstack1l111ll111_opy_ = bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠢိ")
bstack1llll1l111l_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡷࠨࠨࡀ࡫ࠬ࠲࠯࠮ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࢁࡈࡓࠪ࠰࠭ࠦီ"))
bstack1lll1llll11_opy_ = bstack11l1l11_opy_ (u"ࠨࡤࡦࡸࡨࡰࡴࡶ࡭ࡦࡰࡷࠦု")
bstack1ll1lllllll_opy_ = [
    bstack1llll111ll_opy_.bstack111l1ll1l_opy_,
    bstack1llll111ll_opy_.CONNECT,
    bstack1llll111ll_opy_.bstack1ll11111ll_opy_,
]
class SDKCLI:
    _1lll1l1l11l_opy_ = None
    process: Union[None, Any]
    bstack1lll1l11lll_opy_: bool
    bstack1lllll11l1l_opy_: bool
    bstack1llll1lllll_opy_: bool
    bin_session_id: Union[None, str]
    cli_bin_session_id: Union[None, str]
    cli_listen_addr: Union[None, str]
    bstack1llll1ll111_opy_: Union[None, grpc.Channel]
    bstack1lll111l1ll_opy_: str
    test_framework: TestFramework
    bstack1111l11lll_opy_: bstack11111ll1l1_opy_
    session_framework: str
    config: Union[None, Dict[str, Any]]
    bstack1lll11ll11l_opy_: bstack1lll1ll1111_opy_
    accessibility: bstack1lllll11l11_opy_
    ai: bstack1llll111lll_opy_
    bstack1llll1l11ll_opy_: bstack1lll1l11l11_opy_
    bstack1llll111ll1_opy_: List[bstack1lllll1l111_opy_]
    config_testhub: Any
    config_observability: Any
    config_accessibility: Any
    bstack1lll1l1l1ll_opy_: Any
    bstack1lll1l1l1l1_opy_: Dict[str, timedelta]
    bstack1lllll11111_opy_: str
    bstack1111l1llll_opy_: bstack1111l1lll1_opy_
    def __new__(cls):
        if not cls._1lll1l1l11l_opy_:
            cls._1lll1l1l11l_opy_ = super(SDKCLI, cls).__new__(cls)
        return cls._1lll1l1l11l_opy_
    def __init__(self):
        self.process = None
        self.bstack1lll1l11lll_opy_ = False
        self.bstack1llll1ll111_opy_ = None
        self.bstack1lll11lll1l_opy_ = None
        self.cli_bin_session_id = None
        self.cli_listen_addr = os.environ.get(bstack1lll1ll1ll1_opy_, None)
        self.bstack1lll111llll_opy_ = os.environ.get(bstack1llll1l1ll1_opy_, bstack11l1l11_opy_ (u"ࠢࠣူ")) == bstack11l1l11_opy_ (u"ࠣࠤေ")
        self.bstack1lllll11l1l_opy_ = False
        self.bstack1llll1lllll_opy_ = False
        self.config = None
        self.config_testhub = None
        self.config_observability = None
        self.config_accessibility = None
        self.bstack1lll1l1l1ll_opy_ = None
        self.test_framework = None
        self.bstack1111l11lll_opy_ = None
        self.bstack1lll111l1ll_opy_=bstack11l1l11_opy_ (u"ࠤࠥဲ")
        self.session_framework = None
        self.logger = bstack111ll1l11_opy_.get_logger(self.__class__.__name__, bstack111ll1l11_opy_.bstack1lll111ll11_opy_())
        self.bstack1lll1l1l1l1_opy_ = defaultdict(lambda: timedelta(microseconds=0))
        self.bstack1111l1llll_opy_ = bstack1111l1lll1_opy_()
        self.bstack1llll11ll1l_opy_ = None
        self.bstack1llll1l1l1l_opy_ = None
        self.bstack1lll11ll11l_opy_ = None
        self.accessibility = None
        self.ai = None
        self.percy = None
        self.bstack1llll111ll1_opy_ = []
    def bstack1l1l1ll11l_opy_(self):
        return os.environ.get(bstack1l111ll111_opy_).lower().__eq__(bstack11l1l11_opy_ (u"ࠥࡸࡷࡻࡥࠣဳ"))
    def is_enabled(self, config):
        if bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨဴ") in config and str(config[bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩဵ")]).lower() != bstack11l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬံ"):
            return False
        bstack1lll1l1lll1_opy_ = [bstack11l1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ့ࠢ"), bstack11l1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧး")]
        bstack1lll11l11ll_opy_ = config.get(bstack11l1l11_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯္ࠧ")) in bstack1lll1l1lll1_opy_ or os.environ.get(bstack11l1l11_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡕࡔࡇࡇ်ࠫ")) in bstack1lll1l1lll1_opy_
        os.environ[bstack11l1l11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢျ")] = str(bstack1lll11l11ll_opy_) # bstack1lll1l111ll_opy_ bstack1lll11111l1_opy_ VAR to bstack1lllll1lll1_opy_ is binary running
        return bstack1lll11l11ll_opy_
    def bstack1l1l1lll1_opy_(self):
        for event in bstack1ll1lllllll_opy_:
            bstack11l11ll11l_opy_.register(
                event, lambda event_name, *args, **kwargs: bstack11l11ll11l_opy_.logger.debug(bstack11l1l11_opy_ (u"ࠧࢁࡥࡷࡧࡱࡸࡤࡴࡡ࡮ࡧࢀࠤࡂࡄࠠࡼࡣࡵ࡫ࡸࢃࠠࠣြ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢွ"))
            )
        bstack11l11ll11l_opy_.register(bstack1llll111ll_opy_.bstack111l1ll1l_opy_, self.__1lllll111l1_opy_)
        bstack11l11ll11l_opy_.register(bstack1llll111ll_opy_.CONNECT, self.__1llll1lll1l_opy_)
        bstack11l11ll11l_opy_.register(bstack1llll111ll_opy_.bstack1ll11111ll_opy_, self.__1llll1ll1ll_opy_)
        bstack11l11ll11l_opy_.register(bstack1llll111ll_opy_.bstack1l1llllll_opy_, self.__1lllllll1l1_opy_)
    def bstack11llll1l1_opy_(self):
        return not self.bstack1lll111llll_opy_ and os.environ.get(bstack1llll1l1ll1_opy_, bstack11l1l11_opy_ (u"ࠢࠣှ")) != bstack11l1l11_opy_ (u"ࠣࠤဿ")
    def is_running(self):
        if self.bstack1lll111llll_opy_:
            return self.bstack1lll1l11lll_opy_
        else:
            return bool(self.bstack1llll1ll111_opy_)
    def bstack1lll111111l_opy_(self, module):
        return any(isinstance(m, module) for m in self.bstack1llll111ll1_opy_) and cli.is_running()
    def __1lll1111111_opy_(self, bstack1lll1l1ll1l_opy_=10):
        if self.bstack1lll11lll1l_opy_:
            return
        bstack1l1ll1l111_opy_ = datetime.now()
        cli_listen_addr = os.environ.get(bstack1lll1ll1ll1_opy_, self.cli_listen_addr)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡞ࠦ၀") + str(id(self)) + bstack11l1l11_opy_ (u"ࠥࡡࠥࡩ࡯࡯ࡰࡨࡧࡹ࡯࡮ࡨࠤ၁"))
        channel = grpc.insecure_channel(cli_listen_addr, options=[(bstack11l1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠰ࡨࡲࡦࡨ࡬ࡦࡡ࡫ࡸࡹࡶ࡟ࡱࡴࡲࡼࡾࠨ၂"), 0), (bstack11l1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠱ࡩࡳࡧࡢ࡭ࡧࡢ࡬ࡹࡺࡰࡴࡡࡳࡶࡴࡾࡹࠣ၃"), 0)])
        grpc.channel_ready_future(channel).result(timeout=bstack1lll1l1ll1l_opy_)
        self.bstack1llll1ll111_opy_ = channel
        self.bstack1lll11lll1l_opy_ = sdk_pb2_grpc.SDKStub(self.bstack1llll1ll111_opy_)
        self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡨࡵ࡮࡯ࡧࡦࡸࠧ၄"), datetime.now() - bstack1l1ll1l111_opy_)
        self.cli_listen_addr = cli_listen_addr
        os.environ[bstack1lll1ll1ll1_opy_] = self.cli_listen_addr
        self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡱࡩࡨࡺࡥࡥ࠼ࠣ࡭ࡸࡥࡣࡩ࡫࡯ࡨࡤࡶࡲࡰࡥࡨࡷࡸࡃࠢ၅") + str(self.bstack11llll1l1_opy_()) + bstack11l1l11_opy_ (u"ࠣࠤ၆"))
    def __1llll1ll1ll_opy_(self, event_name):
        if self.bstack11llll1l1_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴ࠼ࠣࡷࡹࡵࡰࡱ࡫ࡱ࡫ࠥࡉࡌࡊࠤ၇"))
        self.__1lllllll1ll_opy_()
    def __1lllllll1l1_opy_(self, event_name, bstack1llll1llll1_opy_ = None, bstack1ll1l111ll_opy_=1):
        if bstack1ll1l111ll_opy_ == 1:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩࠥ၈"))
        bstack1lll1l1ll11_opy_ = Path(bstack1lll1l111l1_opy_ (u"ࠦࢀࡹࡥ࡭ࡨ࠱ࡧࡱ࡯࡟ࡥ࡫ࡵࢁ࠴ࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࡹ࠮࡫ࡵࡲࡲࠧ၉"))
        if self.bstack1llllll1111_opy_ and bstack1lll1l1ll11_opy_.exists():
            with open(bstack1lll1l1ll11_opy_, bstack11l1l11_opy_ (u"ࠬࡸࠧ၊"), encoding=bstack11l1l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ။")) as fp:
                data = json.load(fp)
                try:
                    bstack111ll11ll_opy_(bstack11l1l11_opy_ (u"ࠧࡑࡑࡖࡘࠬ၌"), bstack1ll11l11l_opy_(bstack1l11ll11l_opy_), data, {
                        bstack11l1l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭၍"): (self.config[bstack11l1l11_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ၎")], self.config[bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭၏")])
                    })
                except Exception as e:
                    logger.debug(bstack1l1lll1l1_opy_.format(str(e)))
            bstack1lll1l1ll11_opy_.unlink()
        sys.exit(bstack1ll1l111ll_opy_)
    @measure(event_name=EVENTS.bstack1lll1111ll1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1lllll111l1_opy_(self, event_name: str, data):
        from bstack_utils.bstack1l1ll1l11l_opy_ import bstack1lll1llll1l_opy_
        self.bstack1lll111l1ll_opy_, self.bstack1llllll1111_opy_ = bstack1lllll1l1l1_opy_(data.bs_config)
        os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡛ࡗࡏࡔࡂࡄࡏࡉࡤࡊࡉࡓࠩၐ")] = self.bstack1llllll1111_opy_
        if not self.bstack1lll111l1ll_opy_ or not self.bstack1llllll1111_opy_:
            raise ValueError(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡲࡩࠦࡴࡩࡧࠣࡗࡉࡑࠠࡄࡎࡌࠤࡧ࡯࡮ࡢࡴࡼࠦၑ"))
        if self.bstack11llll1l1_opy_():
            self.__1llll1lll1l_opy_(event_name, bstack111111ll1_opy_())
            return
        try:
            bstack1lll1llll1l_opy_.end(EVENTS.bstack1l1l11l1l1_opy_.value, EVENTS.bstack1l1l11l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨၒ"), EVENTS.bstack1l1l11l1l1_opy_.value + bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧၓ"), status=True, failure=None, test_name=None)
            logger.debug(bstack11l1l11_opy_ (u"ࠣࡅࡲࡱࡵࡲࡥࡵࡧࠣࡗࡉࡑࠠࡔࡧࡷࡹࡵ࠴ࠢၔ"))
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡱࡥࡺࠢࡰࡩࡹࡸࡩࡤࡵࠣࡿࢂࠨၕ").format(e))
        start = datetime.now()
        is_started = self.__1lll111l1l1_opy_()
        self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠥࡷࡵࡧࡷ࡯ࡡࡷ࡭ࡲ࡫ࠢၖ"), datetime.now() - start)
        if is_started:
            start = datetime.now()
            self.__1lll1111111_opy_()
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠦࡨࡵ࡮࡯ࡧࡦࡸࡤࡺࡩ࡮ࡧࠥၗ"), datetime.now() - start)
            start = datetime.now()
            self.__1lllll1ll1l_opy_(data)
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡺࡩ࡮ࡧࠥၘ"), datetime.now() - start)
    @measure(event_name=EVENTS.bstack1lll11l111l_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1llll1lll1l_opy_(self, event_name: str, data: bstack111111ll1_opy_):
        if not self.bstack11llll1l1_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶ࠽ࠤࡳࡵࡴࠡࡣࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵࠥၙ"))
            return
        bin_session_id = os.environ.get(bstack1llll1l1ll1_opy_)
        start = datetime.now()
        self.__1lll1111111_opy_()
        self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠢࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨၚ"), datetime.now() - start)
        self.cli_bin_session_id = bin_session_id
        self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡤࡪ࡬ࡰࡩ࠳ࡰࡳࡱࡦࡩࡸࡹ࠺ࠡࡥࡲࡲࡳ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢࡆࡐࡎࠦࠢၛ") + str(bin_session_id) + bstack11l1l11_opy_ (u"ࠤࠥၜ"))
        start = datetime.now()
        self.__1lll1111l1l_opy_()
        self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠥࡷࡹࡧࡲࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡸ࡮ࡳࡥࠣၝ"), datetime.now() - start)
    def __1llll111l1l_opy_(self):
        if not self.bstack1lll11lll1l_opy_ or not self.cli_bin_session_id:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡨࡧ࡮࡯ࡱࡷࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷ࡫ࠠ࡮ࡱࡧࡹࡱ࡫ࡳࠣၞ"))
            return
        bstack1llll11ll11_opy_ = {
            bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤၟ"): (bstack1lll11111ll_opy_, bstack1lllll1llll_opy_, bstack1llllll11ll_opy_),
            bstack11l1l11_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠣၠ"): (bstack1lll1ll11ll_opy_, bstack1lll1lll11l_opy_, bstack1lll1l11ll1_opy_),
        }
        if not self.bstack1llll11ll1l_opy_ and self.session_framework in bstack1llll11ll11_opy_:
            bstack1llllllll1l_opy_, bstack1llllll1l1l_opy_, bstack1lllll111ll_opy_ = bstack1llll11ll11_opy_[self.session_framework]
            bstack1llll11l11l_opy_ = bstack1llllll1l1l_opy_()
            self.bstack1llll1l1l1l_opy_ = bstack1llll11l11l_opy_
            self.bstack1llll11ll1l_opy_ = bstack1lllll111ll_opy_
            self.bstack1llll111ll1_opy_.append(bstack1llll11l11l_opy_)
            self.bstack1llll111ll1_opy_.append(bstack1llllllll1l_opy_(self.bstack1llll1l1l1l_opy_))
        if not self.bstack1lll11ll11l_opy_ and self.config_observability and self.config_observability.success: # bstack1lll11l11l1_opy_
            self.bstack1lll11ll11l_opy_ = bstack1lll1ll1111_opy_(self.bstack1llll11ll1l_opy_, self.bstack1llll1l1l1l_opy_) # bstack1lll11l1ll1_opy_
            self.bstack1llll111ll1_opy_.append(self.bstack1lll11ll11l_opy_)
        if not self.accessibility and self.config_accessibility and self.config_accessibility.success:
            self.accessibility = bstack1lllll11l11_opy_(self.bstack1llll11ll1l_opy_, self.bstack1llll1l1l1l_opy_)
            self.bstack1llll111ll1_opy_.append(self.accessibility)
        if not self.ai and isinstance(self.config, dict) and self.config.get(bstack11l1l11_opy_ (u"ࠢࡴࡧ࡯ࡪࡍ࡫ࡡ࡭ࠤၡ"), False) == True:
            self.ai = bstack1llll111lll_opy_()
            self.bstack1llll111ll1_opy_.append(self.ai)
        if not self.percy and self.bstack1lll1l1l1ll_opy_ and self.bstack1lll1l1l1ll_opy_.success:
            self.percy = bstack1lll1l11l11_opy_(self.bstack1lll1l1l1ll_opy_)
            self.bstack1llll111ll1_opy_.append(self.percy)
        for mod in self.bstack1llll111ll1_opy_:
            if not mod.bstack1llll111l11_opy_():
                mod.configure(self.bstack1lll11lll1l_opy_, self.config, self.cli_bin_session_id, self.bstack1111l1llll_opy_)
    def __1llll1lll11_opy_(self):
        for mod in self.bstack1llll111ll1_opy_:
            if mod.bstack1llll111l11_opy_():
                mod.configure(self.bstack1lll11lll1l_opy_, None, None, None)
    @measure(event_name=EVENTS.bstack1llllllll11_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1lllll1ll1l_opy_(self, data):
        if not self.cli_bin_session_id or self.bstack1lllll11l1l_opy_:
            return
        self.__1llll11l1ll_opy_(data)
        bstack1l1ll1l111_opy_ = datetime.now()
        req = structs.StartBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.path_project = os.getcwd()
        req.language = bstack11l1l11_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣၢ")
        req.sdk_language = bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤၣ")
        req.path_config = data.path_config
        req.sdk_version = data.sdk_version
        req.test_framework = data.test_framework
        req.frameworks.extend(data.frameworks)
        req.framework_versions.update(data.framework_versions)
        req.env_vars.update({key: value for key, value in os.environ.items() if bool(bstack1llll1l111l_opy_.search(key))})
        req.cli_args.extend(sys.argv)
        try:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࠧၤ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠦࡢࠦ࡭ࡢ࡫ࡱ࠱ࡵࡸ࡯ࡤࡧࡶࡷ࠿ࠦࡳࡵࡣࡵࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥၥ"))
            r = self.bstack1lll11lll1l_opy_.StartBinSession(req)
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡹࡧࡲࡵࡡࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴࠢၦ"), datetime.now() - bstack1l1ll1l111_opy_)
            os.environ[bstack1llll1l1ll1_opy_] = r.bin_session_id
            self.__1lll11l1l1l_opy_(r)
            self.__1llll111l1l_opy_()
            self.bstack1111l1llll_opy_.start()
            self.bstack1lllll11l1l_opy_ = True
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡛ࠣၧ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠢ࡞ࠢࡰࡥ࡮ࡴ࠭ࡱࡴࡲࡧࡪࡹࡳ࠻ࠢࡦࡳࡳࡴࡥࡤࡶࡨࡨࠧၨ"))
        except grpc.bstack1lll11lll11_opy_ as bstack1lll1llllll_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣ࡝ࡾ࡭ࡩ࠮ࡳࡦ࡮ࡩ࠭ࢂࡣࠠࡵ࡫ࡰࡩࡴ࡫ࡵࡵ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥၩ") + str(bstack1lll1llllll_opy_) + bstack11l1l11_opy_ (u"ࠤࠥၪ"))
            traceback.print_exc()
            raise bstack1lll1llllll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠥ࡟ࢀ࡯ࡤࠩࡵࡨࡰ࡫࠯ࡽ࡞ࠢࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢၫ") + str(e) + bstack11l1l11_opy_ (u"ࠦࠧၬ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1lll1ll11l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1lll1111l1l_opy_(self):
        if not self.bstack11llll1l1_opy_() or not self.cli_bin_session_id or self.bstack1llll1lllll_opy_:
            return
        bstack1l1ll1l111_opy_ = datetime.now()
        req = structs.ConnectBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        req.platform_index = int(os.environ.get(bstack11l1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬၭ"), bstack11l1l11_opy_ (u"࠭࠰ࠨၮ")))
        try:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡜ࠤၯ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠣ࡟ࠣࡧ࡭࡯࡬ࡥ࠯ࡳࡶࡴࡩࡥࡴࡵ࠽ࠤࡨࡵ࡮࡯ࡧࡦࡸࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠥၰ"))
            r = self.bstack1lll11lll1l_opy_.ConnectBinSession(req)
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡤࡱࡱࡲࡪࡩࡴࡠࡤ࡬ࡲࡤࡹࡥࡴࡵ࡬ࡳࡳࠨၱ"), datetime.now() - bstack1l1ll1l111_opy_)
            self.__1lll11l1l1l_opy_(r)
            self.__1llll111l1l_opy_()
            self.bstack1111l1llll_opy_.start()
            self.bstack1llll1lllll_opy_ = True
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࠧၲ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠦࡢࠦࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡀࠠࡤࡱࡱࡲࡪࡩࡴࡦࡦࠥၳ"))
        except grpc.bstack1lll11lll11_opy_ as bstack1lll1llllll_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠧࡡࡻࡪࡦࠫࡷࡪࡲࡦࠪࡿࡠࠤࡹ࡯࡭ࡦࡱࡨࡹࡹ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢၴ") + str(bstack1lll1llllll_opy_) + bstack11l1l11_opy_ (u"ࠨࠢၵ"))
            traceback.print_exc()
            raise bstack1lll1llllll_opy_
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦၶ") + str(e) + bstack11l1l11_opy_ (u"ࠣࠤၷ"))
            traceback.print_exc()
            raise e
    def __1lll11l1l1l_opy_(self, r):
        self.bstack1llll111111_opy_(r)
        if not r.bin_session_id or not r.config or not isinstance(r.config, str):
            raise ValueError(bstack11l1l11_opy_ (u"ࠤࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡳࡦࡴࡹࡩࡷࠦࡲࡦࡵࡳࡳࡳࡹࡥࠣၸ") + str(r))
        self.config = json.loads(r.config)
        if not self.config:
            raise ValueError(bstack11l1l11_opy_ (u"ࠥࡩࡲࡶࡴࡺࠢࡦࡳࡳ࡬ࡩࡨࠢࡩࡳࡺࡴࡤࠣၹ"))
        self.session_framework = r.session_framework
        self.config_testhub = r.testhub
        self.config_observability = r.observability
        self.config_accessibility = r.accessibility
        bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡨࡶࡨࡿࠠࡪࡵࠣࡷࡪࡴࡴࠡࡱࡱࡰࡾࠦࡡࡴࠢࡳࡥࡷࡺࠠࡰࡨࠣࡸ࡭࡫ࠠࠣࡅࡲࡲࡳ࡫ࡣࡵࡄ࡬ࡲࡘ࡫ࡳࡴ࡫ࡲࡲ࠱ࠨࠠࡢࡰࡧࠤࡹ࡮ࡩࡴࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤ࡮ࡹࠠࡢ࡮ࡶࡳࠥࡻࡳࡦࡦࠣࡦࡾࠦࡓࡵࡣࡵࡸࡇ࡯࡮ࡔࡧࡶࡷ࡮ࡵ࡮࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡘ࡭࡫ࡲࡦࡨࡲࡶࡪ࠲ࠠࡏࡱࡱࡩࠥ࡮ࡡ࡯ࡦ࡯࡭ࡳ࡭ࠠࡪࡵࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹ࡫ࡤ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨၺ")
        self.bstack1lll1l1l1ll_opy_ = getattr(r, bstack11l1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫၻ"), None)
        self.cli_bin_session_id = r.bin_session_id
        os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪၼ")] = self.config_testhub.jwt
        os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬၽ")] = self.config_testhub.build_hashed_id
    def bstack1lll1l1111l_opy_(event_name: EVENTS, stage: STAGE):
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.bstack1lll1l11lll_opy_:
                    return func(self, *args, **kwargs)
                @measure(event_name=event_name, stage=stage)
                def bstack1lll1l11111_opy_(*a, **kw):
                    return func(self, *a, **kw)
                return bstack1lll1l11111_opy_(*args, **kwargs)
            return wrapper
        return decorator
    @bstack1lll1l1111l_opy_(event_name=EVENTS.bstack1llll1l11l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1lll111l1l1_opy_(self, bstack1lll1l1ll1l_opy_=10):
        if self.bstack1lll1l11lll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡵࡷࡥࡷࡺ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡵࡹࡳࡴࡩ࡯ࡩࠥၾ"))
            return True
        self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣၿ"))
        if os.getenv(bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡅࡏࡘࠥႀ")) == bstack1lll1llll11_opy_:
            self.cli_bin_session_id = bstack1lll1llll11_opy_
            self.cli_listen_addr = bstack11l1l11_opy_ (u"ࠦࡺࡴࡩࡹ࠼࠲ࡸࡲࡶ࠯ࡴࡦ࡮࠱ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࠥࡴ࠰ࡶࡳࡨࡱࠢႁ") % (self.cli_bin_session_id)
            self.bstack1lll1l11lll_opy_ = True
            return True
        self.process = subprocess.Popen(
            [self.bstack1lll111l1ll_opy_, bstack11l1l11_opy_ (u"ࠧࡹࡤ࡬ࠤႂ")],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(os.environ),
            text=True,
            universal_newlines=True, # bstack1lll11lllll_opy_ compat for text=True in bstack1lll11ll1l1_opy_ python
            encoding=bstack11l1l11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧႃ"),
            bufsize=1,
            close_fds=True,
        )
        bstack1llllll1ll1_opy_ = threading.Thread(target=self.__1lll1lll111_opy_, args=(bstack1lll1l1ll1l_opy_,))
        bstack1llllll1ll1_opy_.start()
        bstack1llllll1ll1_opy_.join()
        if self.process.returncode is not None:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡳࡱࡣࡺࡲ࠿ࠦࡲࡦࡶࡸࡶࡳࡩ࡯ࡥࡧࡀࡿࡸ࡫࡬ࡧ࠰ࡳࡶࡴࡩࡥࡴࡵ࠱ࡶࡪࡺࡵࡳࡰࡦࡳࡩ࡫ࡽࠡࡱࡸࡸࡂࢁࡳࡦ࡮ࡩ࠲ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡹࡴࡥࡱࡸࡸ࠳ࡸࡥࡢࡦࠫ࠭ࢂࠦࡥࡳࡴࡀࠦႄ") + str(self.process.stderr.read()) + bstack11l1l11_opy_ (u"ࠣࠤႅ"))
        if not self.bstack1lll1l11lll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡞ࠦႆ") + str(id(self)) + bstack11l1l11_opy_ (u"ࠥࡡࠥࡩ࡬ࡦࡣࡱࡹࡵࠨႇ"))
            self.__1lllllll1ll_opy_()
        self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡠࢁࡩࡥࠪࡶࡩࡱ࡬ࠩࡾ࡟ࠣࡴࡷࡵࡣࡦࡵࡶࡣࡷ࡫ࡡࡥࡻ࠽ࠤࠧႈ") + str(self.bstack1lll1l11lll_opy_) + bstack11l1l11_opy_ (u"ࠧࠨႉ"))
        return self.bstack1lll1l11lll_opy_
    def __1lll1lll111_opy_(self, bstack1lll11l1lll_opy_=10):
        bstack1lll1l1l111_opy_ = time.time()
        while self.process and time.time() - bstack1lll1l1l111_opy_ < bstack1lll11l1lll_opy_:
            try:
                line = self.process.stdout.readline()
                if bstack11l1l11_opy_ (u"ࠨࡩࡥ࠿ࠥႊ") in line:
                    self.cli_bin_session_id = line.split(bstack11l1l11_opy_ (u"ࠢࡪࡦࡀࠦႋ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡥ࡯࡭ࡤࡨࡩ࡯ࡡࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࡀࠢႌ") + str(self.cli_bin_session_id) + bstack11l1l11_opy_ (u"ࠤႍࠥ"))
                    continue
                if bstack11l1l11_opy_ (u"ࠥࡰ࡮ࡹࡴࡦࡰࡀࠦႎ") in line:
                    self.cli_listen_addr = line.split(bstack11l1l11_opy_ (u"ࠦࡱ࡯ࡳࡵࡧࡱࡁࠧႏ"))[-1:][0].strip()
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡩ࡬ࡪࡡ࡯࡭ࡸࡺࡥ࡯ࡡࡤࡨࡩࡸ࠺ࠣ႐") + str(self.cli_listen_addr) + bstack11l1l11_opy_ (u"ࠨࠢ႑"))
                    continue
                if bstack11l1l11_opy_ (u"ࠢࡱࡱࡵࡸࡂࠨ႒") in line:
                    port = line.split(bstack11l1l11_opy_ (u"ࠣࡲࡲࡶࡹࡃࠢ႓"))[-1:][0].strip()
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡳࡳࡷࡺ࠺ࠣ႔") + str(port) + bstack11l1l11_opy_ (u"ࠥࠦ႕"))
                    continue
                if line.strip() == bstack1lll1lll1l1_opy_ and self.cli_bin_session_id and self.cli_listen_addr:
                    if os.getenv(bstack11l1l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡍࡔࡥࡓࡕࡔࡈࡅࡒࠨ႖"), bstack11l1l11_opy_ (u"ࠧ࠷ࠢ႗")) == bstack11l1l11_opy_ (u"ࠨ࠱ࠣ႘"):
                        if not self.process.stdout.closed:
                            self.process.stdout.close()
                        if not self.process.stderr.closed:
                            self.process.stderr.close()
                    self.bstack1lll1l11lll_opy_ = True
                    return True
            except Exception as e:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡦࡴࡵࡳࡷࡀࠠࠣ႙") + str(e) + bstack11l1l11_opy_ (u"ࠣࠤႚ"))
        return False
    @measure(event_name=EVENTS.bstack1lll11l1111_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def __1lllllll1ll_opy_(self):
        if self.bstack1llll1ll111_opy_:
            self.bstack1111l1llll_opy_.stop()
            start = datetime.now()
            if self.bstack1lll1ll111l_opy_():
                self.cli_bin_session_id = None
                if self.bstack1llll1lllll_opy_:
                    self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡶ࡬ࡱࡪࠨႛ"), datetime.now() - start)
                else:
                    self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠥࡷࡹࡵࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡷ࡭ࡲ࡫ࠢႜ"), datetime.now() - start)
            self.__1llll1lll11_opy_()
            start = datetime.now()
            self.bstack1llll1ll111_opy_.close()
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠦࡩ࡯ࡳࡤࡱࡱࡲࡪࡩࡴࡠࡶ࡬ࡱࡪࠨႝ"), datetime.now() - start)
            self.bstack1llll1ll111_opy_ = None
        if self.process:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡹࡴࡰࡲࠥ႞"))
            start = datetime.now()
            self.process.terminate()
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠨ࡫ࡪ࡮࡯ࡣࡹ࡯࡭ࡦࠤ႟"), datetime.now() - start)
            self.process = None
            if self.bstack1lll111llll_opy_ and self.config_observability and self.config_testhub and self.config_testhub.testhub_events:
                self.bstack11ll1111l1_opy_()
                self.logger.info(
                    bstack11l1l11_opy_ (u"ࠢࡗ࡫ࡶ࡭ࡹࠦࡨࡵࡶࡳࡷ࠿࠵࠯ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠦࡴࡰࠢࡹ࡭ࡪࡽࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡲࡲࡶࡹ࠲ࠠࡪࡰࡶ࡭࡬࡮ࡴࡴ࠮ࠣࡥࡳࡪࠠ࡮ࡣࡱࡽࠥࡳ࡯ࡳࡧࠣࡨࡪࡨࡵࡨࡩ࡬ࡲ࡬ࠦࡩ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱࠤࡦࡲ࡬ࠡࡣࡷࠤࡴࡴࡥࠡࡲ࡯ࡥࡨ࡫ࠡ࡝ࡰࠥႠ").format(
                        self.config_testhub.build_hashed_id
                    )
                )
                os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧႡ")] = self.config_testhub.build_hashed_id
        self.bstack1lll1l11lll_opy_ = False
    def __1llll11l1ll_opy_(self, data):
        try:
            import selenium
            data.framework_versions[bstack11l1l11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰࠦႢ")] = selenium.__version__
            data.frameworks.append(bstack11l1l11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧႣ"))
        except:
            pass
        try:
            from playwright._repo_version import __version__
            data.framework_versions[bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣႤ")] = __version__
            data.frameworks.append(bstack11l1l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤႥ"))
        except:
            pass
    def bstack1llll11l111_opy_(self, hub_url: str, platform_index: int, bstack1l11111l11_opy_: Any):
        if self.bstack1111l11lll_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡳ࡬࡫ࡳࡴࡪࡪࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡷࡪࡺࠠࡶࡲࠥႦ"))
            return
        try:
            bstack1l1ll1l111_opy_ = datetime.now()
            import selenium
            from selenium.webdriver.remote.webdriver import WebDriver
            from selenium.webdriver.common.service import Service
            framework = bstack11l1l11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠤႧ")
            self.bstack1111l11lll_opy_ = bstack1lll1l11ll1_opy_(
                hub_url,
                platform_index,
                framework_name=framework,
                framework_version=selenium.__version__,
                classes=[WebDriver],
                bstack1lllll1l1ll_opy_={bstack11l1l11_opy_ (u"ࠣࡥࡵࡩࡦࡺࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࡡࡩࡶࡴࡳ࡟ࡤࡣࡳࡷࠧႨ"): bstack1l11111l11_opy_}
            )
            def bstack1lll111l11l_opy_(self):
                return
            if self.config.get(bstack11l1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠦႩ"), True):
                Service.start = bstack1lll111l11l_opy_
                Service.stop = bstack1lll111l11l_opy_
            def get_accessibility_results(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results(driver, framework_name=framework)
            def get_accessibility_results_summary(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.get_accessibility_results_summary(driver, framework_name=framework)
            def perform_scan(driver):
                if self.accessibility and self.accessibility.is_enabled():
                    return self.accessibility.perform_scan(driver, method=None, framework_name=framework)
            WebDriver.getAccessibilityResults = get_accessibility_results
            WebDriver.get_accessibility_results = get_accessibility_results
            WebDriver.getAccessibilityResultsSummary = get_accessibility_results_summary
            WebDriver.get_accessibility_results_summary = get_accessibility_results_summary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠦႪ"), datetime.now() - bstack1l1ll1l111_opy_)
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠻ࠢࠥႫ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨႬ"))
    def bstack1llll1l1111_opy_(self, platform_index: int):
        try:
            from playwright.sync_api import BrowserType
            from playwright.sync_api import BrowserContext
            from playwright._impl._connection import Connection
            from playwright._repo_version import __version__
            from bstack_utils.helper import bstack11llll111_opy_
            self.bstack1111l11lll_opy_ = bstack1llllll11ll_opy_(
                platform_index,
                framework_name=bstack11l1l11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥႭ"),
                framework_version=__version__,
                classes=[BrowserType, BrowserContext, Connection],
            )
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡀࠠࠣႮ") + str(e) + bstack11l1l11_opy_ (u"ࠣࠤႯ"))
            pass
    def bstack1lll1lllll1_opy_(self):
        if self.test_framework:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡶ࡯࡮ࡶࡰࡦࡦࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤࡸ࡫ࡴࠡࡷࡳࠦႰ"))
            return
        if bstack1lll1ll11l_opy_():
            import pytest
            self.test_framework = PytestBDDFramework({ bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶࠥႱ"): pytest.__version__ }, [bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣႲ")])
            return
        try:
            import pytest
            self.test_framework = bstack1llll1111ll_opy_({ bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࠧႳ"): pytest.__version__ }, [bstack11l1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨႴ")])
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࡵࡱࠢࡳࡽࡹ࡫ࡳࡵ࠼ࠣࠦႵ") + str(e) + bstack11l1l11_opy_ (u"ࠣࠤႶ"))
        self.bstack1llllll11l1_opy_()
    def bstack1llllll11l1_opy_(self):
        if not self.bstack1l1l1ll11l_opy_():
            return
        bstack11llll11ll_opy_ = None
        def bstack111lllll_opy_(config, startdir):
            return bstack11l1l11_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢႷ").format(bstack11l1l11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤႸ"))
        def bstack1ll111l11_opy_():
            return
        def bstack1l1lll11_opy_(self, name: str, default=Notset(), skip: bool = False):
            if str(name).lower() == bstack11l1l11_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫႹ"):
                return bstack11l1l11_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦႺ")
            else:
                return bstack11llll11ll_opy_(self, name, default, skip)
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            bstack11llll11ll_opy_ = Config.getoption
            pytest_selenium.pytest_report_header = bstack111lllll_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll111l11_opy_
            Config.getoption = bstack1l1lll11_opy_
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡥࡹࡩࡨࠡࡲࡼࡸࡪࡹࡴࠡࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡀࠠࠣႻ") + str(e) + bstack11l1l11_opy_ (u"ࠢࠣႼ"))
    def bstack1lll1111lll_opy_(self):
        bstack1lllllll11l_opy_ = MessageToDict(cli.config_testhub, preserving_proto_field_name=True)
        if isinstance(bstack1lllllll11l_opy_, dict):
            if cli.config_observability:
                bstack1lllllll11l_opy_.update(
                    {bstack11l1l11_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣႽ"): MessageToDict(cli.config_observability, preserving_proto_field_name=True)}
                )
            if cli.config_accessibility:
                accessibility = MessageToDict(cli.config_accessibility, preserving_proto_field_name=True)
                if isinstance(accessibility, dict) and bstack11l1l11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡶࡣࡹࡵ࡟ࡸࡴࡤࡴࠧႾ") in accessibility.get(bstack11l1l11_opy_ (u"ࠥࡳࡵࡺࡩࡰࡰࡶࠦႿ"), {}):
                    bstack1lll1ll1l11_opy_ = accessibility.get(bstack11l1l11_opy_ (u"ࠦࡴࡶࡴࡪࡱࡱࡷࠧჀ"))
                    bstack1lll1ll1l11_opy_.update({ bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡹࡔࡰ࡙ࡵࡥࡵࠨჁ"): bstack1lll1ll1l11_opy_.pop(bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࡠࡶࡲࡣࡼࡸࡡࡱࠤჂ")) })
                bstack1lllllll11l_opy_.update({bstack11l1l11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢჃ"): accessibility })
        return bstack1lllllll11l_opy_
    @measure(event_name=EVENTS.bstack1lll1lll1ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
    def bstack1lll1ll111l_opy_(self, bstack1lll1111l11_opy_: str = None, bstack1lll11l1l11_opy_: str = None, bstack1ll1l111ll_opy_: int = None):
        if not self.cli_bin_session_id or not self.bstack1lll11lll1l_opy_:
            return
        bstack1l1ll1l111_opy_ = datetime.now()
        req = structs.StopBinSessionRequest()
        req.bin_session_id = self.cli_bin_session_id
        if bstack1ll1l111ll_opy_:
            req.bstack1ll1l111ll_opy_ = bstack1ll1l111ll_opy_
        if bstack1lll1111l11_opy_:
            req.bstack1lll1111l11_opy_ = bstack1lll1111l11_opy_
        if bstack1lll11l1l11_opy_:
            req.bstack1lll11l1l11_opy_ = bstack1lll11l1l11_opy_
        try:
            r = self.bstack1lll11lll1l_opy_.StopBinSession(req)
            self.bstack1ll11lll_opy_(bstack11l1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡵࡱࡳࡣࡧ࡯࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࠤჄ"), datetime.now() - bstack1l1ll1l111_opy_)
            return r.success
        except grpc.RpcError as e:
            traceback.print_exc()
            raise e
    def bstack1ll11lll_opy_(self, key: str, value: timedelta):
        tag = bstack11l1l11_opy_ (u"ࠤࡦ࡬࡮ࡲࡤ࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤჅ") if self.bstack11llll1l1_opy_() else bstack11l1l11_opy_ (u"ࠥࡱࡦ࡯࡮࠮ࡲࡵࡳࡨ࡫ࡳࡴࠤ჆")
        self.bstack1lll1l1l1l1_opy_[bstack11l1l11_opy_ (u"ࠦ࠿ࠨჇ").join([tag + bstack11l1l11_opy_ (u"ࠧ࠳ࠢ჈") + str(id(self)), key])] += value
    def bstack11ll1111l1_opy_(self):
        if not os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡆࡄࡘࡋࡤࡖࡅࡓࡈࠥ჉"), bstack11l1l11_opy_ (u"ࠢ࠱ࠤ჊")) == bstack11l1l11_opy_ (u"ࠣ࠳ࠥ჋"):
            return
        bstack1lll1ll1lll_opy_ = dict()
        bstack1111111111_opy_ = []
        if self.test_framework:
            bstack1111111111_opy_.extend(list(self.test_framework.bstack1111111111_opy_.values()))
        if self.bstack1111l11lll_opy_:
            bstack1111111111_opy_.extend(list(self.bstack1111l11lll_opy_.bstack1111111111_opy_.values()))
        for instance in bstack1111111111_opy_:
            if not instance.platform_index in bstack1lll1ll1lll_opy_:
                bstack1lll1ll1lll_opy_[instance.platform_index] = defaultdict(lambda: timedelta(microseconds=0))
            report = bstack1lll1ll1lll_opy_[instance.platform_index]
            for k, v in instance.bstack1lll1l11l1l_opy_().items():
                report[k] += v
                report[k.split(bstack11l1l11_opy_ (u"ࠤ࠽ࠦ჌"))[0]] += v
        bstack1lllll1l11l_opy_ = sorted([(k, v) for k, v in self.bstack1lll1l1l1l1_opy_.items()], key=lambda o: o[1], reverse=True)
        bstack1llll11111l_opy_ = 0
        for r in bstack1lllll1l11l_opy_:
            bstack1llll1l1l11_opy_ = r[1].total_seconds()
            bstack1llll11111l_opy_ += bstack1llll1l1l11_opy_
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥ࡟ࡵ࡫ࡲࡧ࡟ࠣࡧࡱ࡯࠺ࡼࡴ࡞࠴ࡢࢃ࠽ࠣჍ") + str(bstack1llll1l1l11_opy_) + bstack11l1l11_opy_ (u"ࠦࠧ჎"))
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࠳࠭ࠣ჏"))
        bstack1lllllllll1_opy_ = []
        for platform_index, report in bstack1lll1ll1lll_opy_.items():
            bstack1lllllllll1_opy_.extend([(platform_index, k, v) for k, v in report.items()])
        bstack1lllllllll1_opy_.sort(key=lambda o: o[2], reverse=True)
        bstack1llll1l11_opy_ = set()
        bstack1lllll11ll1_opy_ = 0
        for r in bstack1lllllllll1_opy_:
            bstack1llll1l1l11_opy_ = r[2].total_seconds()
            bstack1lllll11ll1_opy_ += bstack1llll1l1l11_opy_
            bstack1llll1l11_opy_.add(r[0])
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡛ࡱࡧࡵࡪࡢࠦࡴࡦࡵࡷ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࠳ࡻࡳ࡝࠳ࡡࢂࡀࡻࡳ࡝࠴ࡡࢂࡃࠢა") + str(bstack1llll1l1l11_opy_) + bstack11l1l11_opy_ (u"ࠢࠣბ"))
        if self.bstack11llll1l1_opy_():
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࠯࠰ࠦგ"))
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤ࡞ࡴࡪࡸࡦ࡞ࠢࡦࡰ࡮ࡀࡣࡩ࡫࡯ࡨ࠲ࡶࡲࡰࡥࡨࡷࡸࡃࡻࡵࡱࡷࡥࡱࡥࡣ࡭࡫ࢀࠤࡹ࡫ࡳࡵ࠼ࡳࡰࡦࡺࡦࡰࡴࡰࡷ࠲ࢁࡳࡵࡴࠫࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠯ࡽ࠾ࠤდ") + str(bstack1lllll11ll1_opy_) + bstack11l1l11_opy_ (u"ࠥࠦე"))
        else:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡠࡶࡥࡳࡨࡠࠤࡨࡲࡩ࠻࡯ࡤ࡭ࡳ࠳ࡰࡳࡱࡦࡩࡸࡹ࠽ࠣვ") + str(bstack1llll11111l_opy_) + bstack11l1l11_opy_ (u"ࠧࠨზ"))
        self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࠭࠮ࠤთ"))
    def bstack1llll111111_opy_(self, r):
        if r is not None and getattr(r, bstack11l1l11_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࠨი"), None) and getattr(r.testhub, bstack11l1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨკ"), None):
            errors = json.loads(r.testhub.errors.decode(bstack11l1l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣლ")))
            for bstack1llllll111l_opy_, err in errors.items():
                if err[bstack11l1l11_opy_ (u"ࠪࡸࡾࡶࡥࠨმ")] == bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡦࡰࠩნ"):
                    self.logger.info(err[bstack11l1l11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ო")])
                else:
                    self.logger.error(err[bstack11l1l11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧპ")])
cli = SDKCLI()