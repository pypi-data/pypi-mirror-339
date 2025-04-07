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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11lll1lll1l_opy_, bstack1llll1ll11_opy_, bstack11ll1ll1l1_opy_, bstack11ll1ll11_opy_,
                                    bstack11lllllll11_opy_, bstack11llllll11l_opy_, bstack11llll1ll11_opy_, bstack11lll1llll1_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1l111ll1_opy_, bstack111l1llll_opy_
from bstack_utils.proxy import bstack1ll11lll1_opy_, bstack11ll1l1l1_opy_
from bstack_utils.constants import *
from bstack_utils import bstack111ll1l11_opy_
from browserstack_sdk._version import __version__
bstack111ll1lll_opy_ = Config.bstack111l1l1l_opy_()
logger = bstack111ll1l11_opy_.get_logger(__name__, bstack111ll1l11_opy_.bstack1lll111ll11_opy_())
def bstack1l111l11l11_opy_(config):
    return config[bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬᤏ")]
def bstack1l1111l1l1l_opy_(config):
    return config[bstack11l1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧᤐ")]
def bstack1l1l111ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11lll111ll1_opy_(obj):
    values = []
    bstack11ll111lll1_opy_ = re.compile(bstack11l1l11_opy_ (u"ࡷࠨ࡞ࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣࡡࡪࠫࠥࠤᤑ"), re.I)
    for key in obj.keys():
        if bstack11ll111lll1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11lll1ll111_opy_(config):
    tags = []
    tags.extend(bstack11lll111ll1_opy_(os.environ))
    tags.extend(bstack11lll111ll1_opy_(config))
    return tags
def bstack11lll1l1l11_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11ll1111ll1_opy_(bstack11ll111ll11_opy_):
    if not bstack11ll111ll11_opy_:
        return bstack11l1l11_opy_ (u"࠭ࠧᤒ")
    return bstack11l1l11_opy_ (u"ࠢࡼࡿࠣࠬࢀࢃࠩࠣᤓ").format(bstack11ll111ll11_opy_.name, bstack11ll111ll11_opy_.email)
def bstack1l111l111l1_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll1lll111_opy_ = repo.common_dir
        info = {
            bstack11l1l11_opy_ (u"ࠣࡵ࡫ࡥࠧᤔ"): repo.head.commit.hexsha,
            bstack11l1l11_opy_ (u"ࠤࡶ࡬ࡴࡸࡴࡠࡵ࡫ࡥࠧᤕ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11l1l11_opy_ (u"ࠥࡦࡷࡧ࡮ࡤࡪࠥᤖ"): repo.active_branch.name,
            bstack11l1l11_opy_ (u"ࠦࡹࡧࡧࠣᤗ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡹ࡫ࡲࠣᤘ"): bstack11ll1111ll1_opy_(repo.head.commit.committer),
            bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࡡࡧࡥࡹ࡫ࠢᤙ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11l1l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡴࡸࠢᤚ"): bstack11ll1111ll1_opy_(repo.head.commit.author),
            bstack11l1l11_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࡠࡦࡤࡸࡪࠨᤛ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11l1l11_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥᤜ"): repo.head.commit.message,
            bstack11l1l11_opy_ (u"ࠥࡶࡴࡵࡴࠣᤝ"): repo.git.rev_parse(bstack11l1l11_opy_ (u"ࠦ࠲࠳ࡳࡩࡱࡺ࠱ࡹࡵࡰ࡭ࡧࡹࡩࡱࠨᤞ")),
            bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡲࡲࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨ᤟"): bstack11ll1lll111_opy_,
            bstack11l1l11_opy_ (u"ࠨࡷࡰࡴ࡮ࡸࡷ࡫ࡥࡠࡩ࡬ࡸࡤࡪࡩࡳࠤᤠ"): subprocess.check_output([bstack11l1l11_opy_ (u"ࠢࡨ࡫ࡷࠦᤡ"), bstack11l1l11_opy_ (u"ࠣࡴࡨࡺ࠲ࡶࡡࡳࡵࡨࠦᤢ"), bstack11l1l11_opy_ (u"ࠤ࠰࠱࡬࡯ࡴ࠮ࡥࡲࡱࡲࡵ࡮࠮ࡦ࡬ࡶࠧᤣ")]).strip().decode(
                bstack11l1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᤤ")),
            bstack11l1l11_opy_ (u"ࠦࡱࡧࡳࡵࡡࡷࡥ࡬ࠨᤥ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11l1l11_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡸࡥࡳࡪࡰࡦࡩࡤࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᤦ"): repo.git.rev_list(
                bstack11l1l11_opy_ (u"ࠨࡻࡾ࠰࠱ࡿࢂࠨᤧ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll11lll1l_opy_ = []
        for remote in remotes:
            bstack11ll11111l1_opy_ = {
                bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᤨ"): remote.name,
                bstack11l1l11_opy_ (u"ࠣࡷࡵࡰࠧᤩ"): remote.url,
            }
            bstack11ll11lll1l_opy_.append(bstack11ll11111l1_opy_)
        bstack11ll11ll1ll_opy_ = {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᤪ"): bstack11l1l11_opy_ (u"ࠥ࡫࡮ࡺࠢᤫ"),
            **info,
            bstack11l1l11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨࡷࠧ᤬"): bstack11ll11lll1l_opy_
        }
        bstack11ll11ll1ll_opy_ = bstack11ll1llll1l_opy_(bstack11ll11ll1ll_opy_)
        return bstack11ll11ll1ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡵࡰࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡉ࡬ࡸࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣ᤭").format(err))
        return {}
def bstack11ll1llll1l_opy_(bstack11ll11ll1ll_opy_):
    bstack11ll1llllll_opy_ = bstack11l1llll1ll_opy_(bstack11ll11ll1ll_opy_)
    if bstack11ll1llllll_opy_ and bstack11ll1llllll_opy_ > bstack11lllllll11_opy_:
        bstack11ll1l1ll1l_opy_ = bstack11ll1llllll_opy_ - bstack11lllllll11_opy_
        bstack11ll11l1lll_opy_ = bstack11ll1l1l1l1_opy_(bstack11ll11ll1ll_opy_[bstack11l1l11_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢ᤮")], bstack11ll1l1ll1l_opy_)
        bstack11ll11ll1ll_opy_[bstack11l1l11_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣ᤯")] = bstack11ll11l1lll_opy_
        logger.info(bstack11l1l11_opy_ (u"ࠣࡖ࡫ࡩࠥࡩ࡯࡮࡯࡬ࡸࠥ࡮ࡡࡴࠢࡥࡩࡪࡴࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦ࠱ࠤࡘ࡯ࡺࡦࠢࡲࡪࠥࡩ࡯࡮࡯࡬ࡸࠥࡧࡦࡵࡧࡵࠤࡹࡸࡵ࡯ࡥࡤࡸ࡮ࡵ࡮ࠡ࡫ࡶࠤࢀࢃࠠࡌࡄࠥᤰ")
                    .format(bstack11l1llll1ll_opy_(bstack11ll11ll1ll_opy_) / 1024))
    return bstack11ll11ll1ll_opy_
def bstack11l1llll1ll_opy_(bstack1llllll1ll_opy_):
    try:
        if bstack1llllll1ll_opy_:
            bstack11ll1lll11l_opy_ = json.dumps(bstack1llllll1ll_opy_)
            bstack11ll1l1ll11_opy_ = sys.getsizeof(bstack11ll1lll11l_opy_)
            return bstack11ll1l1ll11_opy_
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠤࡖࡳࡲ࡫ࡴࡩ࡫ࡱ࡫ࠥࡽࡥ࡯ࡶࠣࡻࡷࡵ࡮ࡨࠢࡺ࡬࡮ࡲࡥࠡࡥࡤࡰࡨࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡳࡪࡼࡨࠤࡴ࡬ࠠࡋࡕࡒࡒࠥࡵࡢ࡫ࡧࡦࡸ࠿ࠦࡻࡾࠤᤱ").format(e))
    return -1
def bstack11ll1l1l1l1_opy_(field, bstack11lll11lll1_opy_):
    try:
        bstack11lll11l1ll_opy_ = len(bytes(bstack11llllll11l_opy_, bstack11l1l11_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᤲ")))
        bstack11ll11ll11l_opy_ = bytes(field, bstack11l1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᤳ"))
        bstack11lll11111l_opy_ = len(bstack11ll11ll11l_opy_)
        bstack11ll1ll1l1l_opy_ = ceil(bstack11lll11111l_opy_ - bstack11lll11lll1_opy_ - bstack11lll11l1ll_opy_)
        if bstack11ll1ll1l1l_opy_ > 0:
            bstack11ll1llll11_opy_ = bstack11ll11ll11l_opy_[:bstack11ll1ll1l1l_opy_].decode(bstack11l1l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᤴ"), errors=bstack11l1l11_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪ࠭ᤵ")) + bstack11llllll11l_opy_
            return bstack11ll1llll11_opy_
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡺࡲࡶࡰࡦࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡪࡲࡤ࠭ࠢࡱࡳࡹ࡮ࡩ࡯ࡩࠣࡻࡦࡹࠠࡵࡴࡸࡲࡨࡧࡴࡦࡦࠣ࡬ࡪࡸࡥ࠻ࠢࡾࢁࠧᤶ").format(e))
    return field
def bstack1ll1lllll1_opy_():
    env = os.environ
    if (bstack11l1l11_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᤷ") in env and len(env[bstack11l1l11_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢ࡙ࡗࡒࠢᤸ")]) > 0) or (
            bstack11l1l11_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤ᤹") in env and len(env[bstack11l1l11_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤࡎࡏࡎࡇࠥ᤺")]) > 0):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧ᤻ࠥ"): bstack11l1l11_opy_ (u"ࠨࡊࡦࡰ࡮࡭ࡳࡹࠢ᤼"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᤽"): env.get(bstack11l1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᤾")),
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᤿"): env.get(bstack11l1l11_opy_ (u"ࠥࡎࡔࡈ࡟ࡏࡃࡐࡉࠧ᥀")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᥁"): env.get(bstack11l1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦ᥂"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡃࡊࠤ᥃")) == bstack11l1l11_opy_ (u"ࠢࡵࡴࡸࡩࠧ᥄") and bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡄࡋࠥ᥅"))):
        return {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᥆"): bstack11l1l11_opy_ (u"ࠥࡇ࡮ࡸࡣ࡭ࡧࡆࡍࠧ᥇"),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᥈"): env.get(bstack11l1l11_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣ᥉")),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᥊"): env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡋࡑࡅࠦ᥋")),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ᥌"): env.get(bstack11l1l11_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࠧ᥍"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࠨ᥎")) == bstack11l1l11_opy_ (u"ࠦࡹࡸࡵࡦࠤ᥏") and bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࠧᥐ"))):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᥑ"): bstack11l1l11_opy_ (u"ࠢࡕࡴࡤࡺ࡮ࡹࠠࡄࡋࠥᥒ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᥓ"): env.get(bstack11l1l11_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠ࡙ࡈࡆࡤ࡛ࡒࡍࠤᥔ")),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᥕ"): env.get(bstack11l1l11_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᥖ")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᥗ"): env.get(bstack11l1l11_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᥘ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࠥᥙ")) == bstack11l1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨᥚ") and env.get(bstack11l1l11_opy_ (u"ࠤࡆࡍࡤࡔࡁࡎࡇࠥᥛ")) == bstack11l1l11_opy_ (u"ࠥࡧࡴࡪࡥࡴࡪ࡬ࡴࠧᥜ"):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᥝ"): bstack11l1l11_opy_ (u"ࠧࡉ࡯ࡥࡧࡶ࡬࡮ࡶࠢᥞ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᥟ"): None,
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᥠ"): None,
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᥡ"): None
        }
    if env.get(bstack11l1l11_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡒࡂࡐࡆࡌࠧᥢ")) and env.get(bstack11l1l11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡃࡐࡏࡐࡍ࡙ࠨᥣ")):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᥤ"): bstack11l1l11_opy_ (u"ࠧࡈࡩࡵࡤࡸࡧࡰ࡫ࡴࠣᥥ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᥦ"): env.get(bstack11l1l11_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡋࡎ࡚࡟ࡉࡖࡗࡔࡤࡕࡒࡊࡉࡌࡒࠧᥧ")),
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᥨ"): None,
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᥩ"): env.get(bstack11l1l11_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᥪ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠦࡈࡏࠢᥫ")) == bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᥬ") and bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠨࡄࡓࡑࡑࡉࠧᥭ"))):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᥮"): bstack11l1l11_opy_ (u"ࠣࡆࡵࡳࡳ࡫ࠢ᥯"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᥰ"): env.get(bstack11l1l11_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡎࡌࡒࡐࠨᥱ")),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᥲ"): None,
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᥳ"): env.get(bstack11l1l11_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᥴ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࠥ᥵")) == bstack11l1l11_opy_ (u"ࠣࡶࡵࡹࡪࠨ᥶") and bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࠧ᥷"))):
        return {
            bstack11l1l11_opy_ (u"ࠥࡲࡦࡳࡥࠣ᥸"): bstack11l1l11_opy_ (u"ࠦࡘ࡫࡭ࡢࡲ࡫ࡳࡷ࡫ࠢ᥹"),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᥺"): env.get(bstack11l1l11_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡒࡖࡌࡇࡎࡊ࡜ࡄࡘࡎࡕࡎࡠࡗࡕࡐࠧ᥻")),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᥼"): env.get(bstack11l1l11_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᥽")),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᥾"): env.get(bstack11l1l11_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡍࡉࠨ᥿"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠦࡈࡏࠢᦀ")) == bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᦁ") and bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠨࡇࡊࡖࡏࡅࡇࡥࡃࡊࠤᦂ"))):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦃ"): bstack11l1l11_opy_ (u"ࠣࡉ࡬ࡸࡑࡧࡢࠣᦄ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᦅ"): env.get(bstack11l1l11_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢ࡙ࡗࡒࠢᦆ")),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᦇ"): env.get(bstack11l1l11_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥᦈ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦉ"): env.get(bstack11l1l11_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡊࡆࠥᦊ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠣࡅࡌࠦᦋ")) == bstack11l1l11_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᦌ") and bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࠨᦍ"))):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᦎ"): bstack11l1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧ࡯࡮ࡺࡥࠣᦏ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᦐ"): env.get(bstack11l1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᦑ")),
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᦒ"): env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡒࡁࡃࡇࡏࠦᦓ")) or env.get(bstack11l1l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᦔ")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᦕ"): env.get(bstack11l1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᦖ"))
        }
    if bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᦗ"))):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᦘ"): bstack11l1l11_opy_ (u"ࠣࡘ࡬ࡷࡺࡧ࡬ࠡࡕࡷࡹࡩ࡯࡯ࠡࡖࡨࡥࡲࠦࡓࡦࡴࡹ࡭ࡨ࡫ࡳࠣᦙ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᦚ"): bstack11l1l11_opy_ (u"ࠥࡿࢂࢁࡽࠣᦛ").format(env.get(bstack11l1l11_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᦜ")), env.get(bstack11l1l11_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࡌࡈࠬᦝ"))),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᦞ"): env.get(bstack11l1l11_opy_ (u"ࠢࡔ࡛ࡖࡘࡊࡓ࡟ࡅࡇࡉࡍࡓࡏࡔࡊࡑࡑࡍࡉࠨᦟ")),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᦠ"): env.get(bstack11l1l11_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᦡ"))
        }
    if bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࠧᦢ"))):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᦣ"): bstack11l1l11_opy_ (u"ࠧࡇࡰࡱࡸࡨࡽࡴࡸࠢᦤ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᦥ"): bstack11l1l11_opy_ (u"ࠢࡼࡿ࠲ࡴࡷࡵࡪࡦࡥࡷ࠳ࢀࢃ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂࠨᦦ").format(env.get(bstack11l1l11_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢ࡙ࡗࡒࠧᦧ")), env.get(bstack11l1l11_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡆࡉࡃࡐࡗࡑࡘࡤࡔࡁࡎࡇࠪᦨ")), env.get(bstack11l1l11_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡓࡍࡗࡊࠫᦩ")), env.get(bstack11l1l11_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨᦪ"))),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᦫ"): env.get(bstack11l1l11_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ᦬")),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᦭"): env.get(bstack11l1l11_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᦮"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠤࡄ࡞࡚ࡘࡅࡠࡊࡗࡘࡕࡥࡕࡔࡇࡕࡣࡆࡍࡅࡏࡖࠥ᦯")) and env.get(bstack11l1l11_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧᦰ")):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᦱ"): bstack11l1l11_opy_ (u"ࠧࡇࡺࡶࡴࡨࠤࡈࡏࠢᦲ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᦳ"): bstack11l1l11_opy_ (u"ࠢࡼࡿࡾࢁ࠴ࡥࡢࡶ࡫࡯ࡨ࠴ࡸࡥࡴࡷ࡯ࡸࡸࡅࡢࡶ࡫࡯ࡨࡎࡪ࠽ࡼࡿࠥᦴ").format(env.get(bstack11l1l11_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫᦵ")), env.get(bstack11l1l11_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࠧᦶ")), env.get(bstack11l1l11_opy_ (u"ࠪࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠪᦷ"))),
            bstack11l1l11_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᦸ"): env.get(bstack11l1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᦹ")),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᦺ"): env.get(bstack11l1l11_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᦻ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᦼ")), env.get(bstack11l1l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡘࡅࡔࡑࡏ࡚ࡊࡊ࡟ࡔࡑࡘࡖࡈࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࠣᦽ")), env.get(bstack11l1l11_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢᦾ"))]):
        return {
            bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᦿ"): bstack11l1l11_opy_ (u"ࠧࡇࡗࡔࠢࡆࡳࡩ࡫ࡂࡶ࡫࡯ࡨࠧᧀ"),
            bstack11l1l11_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᧁ"): env.get(bstack11l1l11_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡔ࡚ࡈࡌࡊࡅࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᧂ")),
            bstack11l1l11_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᧃ"): env.get(bstack11l1l11_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᧄ")),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᧅ"): env.get(bstack11l1l11_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᧆ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥᧇ")):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᧈ"): bstack11l1l11_opy_ (u"ࠢࡃࡣࡰࡦࡴࡵࠢᧉ"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᧊"): env.get(bstack11l1l11_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡓࡧࡶࡹࡱࡺࡳࡖࡴ࡯ࠦ᧋")),
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᧌"): env.get(bstack11l1l11_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡸ࡮࡯ࡳࡶࡍࡳࡧࡔࡡ࡮ࡧࠥ᧍")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᧎"): env.get(bstack11l1l11_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡓࡻ࡭ࡣࡧࡵࠦ᧏"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࠣ᧐")) or env.get(bstack11l1l11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ᧑")):
        return {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧒"): bstack11l1l11_opy_ (u"࡛ࠥࡪࡸࡣ࡬ࡧࡵࠦ᧓"),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᧔"): env.get(bstack11l1l11_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ᧕")),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣ᧖"): bstack11l1l11_opy_ (u"ࠢࡎࡣ࡬ࡲࠥࡖࡩࡱࡧ࡯࡭ࡳ࡫ࠢ᧗") if env.get(bstack11l1l11_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡐࡅࡎࡔ࡟ࡑࡋࡓࡉࡑࡏࡎࡆࡡࡖࡘࡆࡘࡔࡆࡆࠥ᧘")) else None,
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧙"): env.get(bstack11l1l11_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡌࡏࡔࡠࡅࡒࡑࡒࡏࡔࠣ᧚"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠦࡌࡉࡐࡠࡒࡕࡓࡏࡋࡃࡕࠤ᧛")), env.get(bstack11l1l11_opy_ (u"ࠧࡍࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᧜")), env.get(bstack11l1l11_opy_ (u"ࠨࡇࡐࡑࡊࡐࡊࡥࡃࡍࡑࡘࡈࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ᧝"))]):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧞"): bstack11l1l11_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡅ࡯ࡳࡺࡪࠢ᧟"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧠"): None,
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ᧡"): env.get(bstack11l1l11_opy_ (u"ࠦࡕࡘࡏࡋࡇࡆࡘࡤࡏࡄࠣ᧢")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ᧣"): env.get(bstack11l1l11_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡏࡄࠣ᧤"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࠥ᧥")):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᧦"): bstack11l1l11_opy_ (u"ࠤࡖ࡬࡮ࡶࡰࡢࡤ࡯ࡩࠧ᧧"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᧨"): env.get(bstack11l1l11_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᧩")),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧪"): bstack11l1l11_opy_ (u"ࠨࡊࡰࡤࠣࠧࢀࢃࠢ᧫").format(env.get(bstack11l1l11_opy_ (u"ࠧࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠪ᧬"))) if env.get(bstack11l1l11_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡏࡕࡂࡠࡋࡇࠦ᧭")) else None,
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᧮"): env.get(bstack11l1l11_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᧯"))
        }
    if bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠦࡓࡋࡔࡍࡋࡉ࡝ࠧ᧰"))):
        return {
            bstack11l1l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ᧱"): bstack11l1l11_opy_ (u"ࠨࡎࡦࡶ࡯࡭࡫ࡿࠢ᧲"),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᧳"): env.get(bstack11l1l11_opy_ (u"ࠣࡆࡈࡔࡑࡕ࡙ࡠࡗࡕࡐࠧ᧴")),
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᧵"): env.get(bstack11l1l11_opy_ (u"ࠥࡗࡎ࡚ࡅࡠࡐࡄࡑࡊࠨ᧶")),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᧷"): env.get(bstack11l1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢ᧸"))
        }
    if bstack1ll11l1l1_opy_(env.get(bstack11l1l11_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡁࡄࡖࡌࡓࡓ࡙ࠢ᧹"))):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧺"): bstack11l1l11_opy_ (u"ࠣࡉ࡬ࡸࡍࡻࡢࠡࡃࡦࡸ࡮ࡵ࡮ࡴࠤ᧻"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧼"): bstack11l1l11_opy_ (u"ࠥࡿࢂ࠵ࡻࡾ࠱ࡤࡧࡹ࡯࡯࡯ࡵ࠲ࡶࡺࡴࡳ࠰ࡽࢀࠦ᧽").format(env.get(bstack11l1l11_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡘࡋࡒࡗࡇࡕࡣ࡚ࡘࡌࠨ᧾")), env.get(bstack11l1l11_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡅࡑࡑࡖࡍ࡙ࡕࡒ࡚ࠩ᧿")), env.get(bstack11l1l11_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉ࠭ᨀ"))),
            bstack11l1l11_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᨁ"): env.get(bstack11l1l11_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠ࡙ࡒࡖࡐࡌࡌࡐ࡙ࠥᨂ")),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨃ"): env.get(bstack11l1l11_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠥᨄ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠦࡈࡏࠢᨅ")) == bstack11l1l11_opy_ (u"ࠧࡺࡲࡶࡧࠥᨆ") and env.get(bstack11l1l11_opy_ (u"ࠨࡖࡆࡔࡆࡉࡑࠨᨇ")) == bstack11l1l11_opy_ (u"ࠢ࠲ࠤᨈ"):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᨉ"): bstack11l1l11_opy_ (u"ࠤ࡙ࡩࡷࡩࡥ࡭ࠤᨊ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᨋ"): bstack11l1l11_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࢀࢃࠢᨌ").format(env.get(bstack11l1l11_opy_ (u"ࠬ࡜ࡅࡓࡅࡈࡐࡤ࡛ࡒࡍࠩᨍ"))),
            bstack11l1l11_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨎ"): None,
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨏ"): None,
        }
    if env.get(bstack11l1l11_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᨐ")):
        return {
            bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨑ"): bstack11l1l11_opy_ (u"ࠥࡘࡪࡧ࡭ࡤ࡫ࡷࡽࠧᨒ"),
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨓ"): None,
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᨔ"): env.get(bstack11l1l11_opy_ (u"ࠨࡔࡆࡃࡐࡇࡎ࡚࡙ࡠࡒࡕࡓࡏࡋࡃࡕࡡࡑࡅࡒࡋࠢᨕ")),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨖ"): env.get(bstack11l1l11_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᨗ"))
        }
    if any([env.get(bstack11l1l11_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉᨘࠧ")), env.get(bstack11l1l11_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡓࡎࠥᨙ")), env.get(bstack11l1l11_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠤᨚ")), env.get(bstack11l1l11_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡖࡈࡅࡒࠨᨛ"))]):
        return {
            bstack11l1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ᨜"): bstack11l1l11_opy_ (u"ࠢࡄࡱࡱࡧࡴࡻࡲࡴࡧࠥ᨝"),
            bstack11l1l11_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ᨞"): None,
            bstack11l1l11_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᨟"): env.get(bstack11l1l11_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᨠ")) or None,
            bstack11l1l11_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨡ"): env.get(bstack11l1l11_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢᨢ"), 0)
        }
    if env.get(bstack11l1l11_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦᨣ")):
        return {
            bstack11l1l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᨤ"): bstack11l1l11_opy_ (u"ࠣࡉࡲࡇࡉࠨᨥ"),
            bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᨦ"): None,
            bstack11l1l11_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨧ"): env.get(bstack11l1l11_opy_ (u"ࠦࡌࡕ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᨨ")),
            bstack11l1l11_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᨩ"): env.get(bstack11l1l11_opy_ (u"ࠨࡇࡐࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡈࡕࡕࡏࡖࡈࡖࠧᨪ"))
        }
    if env.get(bstack11l1l11_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᨫ")):
        return {
            bstack11l1l11_opy_ (u"ࠣࡰࡤࡱࡪࠨᨬ"): bstack11l1l11_opy_ (u"ࠤࡆࡳࡩ࡫ࡆࡳࡧࡶ࡬ࠧᨭ"),
            bstack11l1l11_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᨮ"): env.get(bstack11l1l11_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᨯ")),
            bstack11l1l11_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᨰ"): env.get(bstack11l1l11_opy_ (u"ࠨࡃࡇࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᨱ")),
            bstack11l1l11_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨲ"): env.get(bstack11l1l11_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨᨳ"))
        }
    return {bstack11l1l11_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᨴ"): None}
def get_host_info():
    return {
        bstack11l1l11_opy_ (u"ࠥ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠧᨵ"): platform.node(),
        bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨᨶ"): platform.system(),
        bstack11l1l11_opy_ (u"ࠧࡺࡹࡱࡧࠥᨷ"): platform.machine(),
        bstack11l1l11_opy_ (u"ࠨࡶࡦࡴࡶ࡭ࡴࡴࠢᨸ"): platform.version(),
        bstack11l1l11_opy_ (u"ࠢࡢࡴࡦ࡬ࠧᨹ"): platform.architecture()[0]
    }
def bstack1lll1l1ll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11ll1lll1ll_opy_():
    if bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩᨺ")):
        return bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᨻ")
    return bstack11l1l11_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠩᨼ")
def bstack11ll1l1111l_opy_(driver):
    info = {
        bstack11l1l11_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᨽ"): driver.capabilities,
        bstack11l1l11_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠩᨾ"): driver.session_id,
        bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᨿ"): driver.capabilities.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᩀ"), None),
        bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᩁ"): driver.capabilities.get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᩂ"), None),
        bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬᩃ"): driver.capabilities.get(bstack11l1l11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᩄ"), None),
        bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᩅ"):driver.capabilities.get(bstack11l1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᩆ"), None),
    }
    if bstack11ll1lll1ll_opy_() == bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᩇ"):
        if bstack1llll11111_opy_():
            info[bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩᩈ")] = bstack11l1l11_opy_ (u"ࠩࡤࡴࡵ࠳ࡡࡶࡶࡲࡱࡦࡺࡥࠨᩉ")
        elif driver.capabilities.get(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᩊ"), {}).get(bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨᩋ"), False):
            info[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ᩌ")] = bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᩍ")
        else:
            info[bstack11l1l11_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨᩎ")] = bstack11l1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪᩏ")
    return info
def bstack1llll11111_opy_():
    if bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨᩐ")):
        return True
    if bstack1ll11l1l1_opy_(os.environ.get(bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫᩑ"), None)):
        return True
    return False
def bstack111ll11ll_opy_(bstack11ll1l11lll_opy_, url, data, config):
    headers = config.get(bstack11l1l11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᩒ"), None)
    proxies = bstack1ll11lll1_opy_(config, url)
    auth = config.get(bstack11l1l11_opy_ (u"ࠬࡧࡵࡵࡪࠪᩓ"), None)
    response = requests.request(
            bstack11ll1l11lll_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1111l1ll_opy_(bstack11ll1ll1l_opy_, size):
    bstack1llllllll_opy_ = []
    while len(bstack11ll1ll1l_opy_) > size:
        bstack1111ll1l1_opy_ = bstack11ll1ll1l_opy_[:size]
        bstack1llllllll_opy_.append(bstack1111ll1l1_opy_)
        bstack11ll1ll1l_opy_ = bstack11ll1ll1l_opy_[size:]
    bstack1llllllll_opy_.append(bstack11ll1ll1l_opy_)
    return bstack1llllllll_opy_
def bstack11lll1l1ll1_opy_(message, bstack11l1lll1lll_opy_=False):
    os.write(1, bytes(message, bstack11l1l11_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᩔ")))
    os.write(1, bytes(bstack11l1l11_opy_ (u"ࠧ࡝ࡰࠪᩕ"), bstack11l1l11_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᩖ")))
    if bstack11l1lll1lll_opy_:
        with open(bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠯ࡲ࠵࠶ࡿ࠭ࠨᩗ") + os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᩘ")] + bstack11l1l11_opy_ (u"ࠫ࠳ࡲ࡯ࡨࠩᩙ"), bstack11l1l11_opy_ (u"ࠬࡧࠧᩚ")) as f:
            f.write(message + bstack11l1l11_opy_ (u"࠭࡜࡯ࠩᩛ"))
def bstack1ll1111l1ll_opy_():
    return os.environ[bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡖࡖࡒࡑࡆ࡚ࡉࡐࡐࠪᩜ")].lower() == bstack11l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᩝ")
def bstack1ll11l11l_opy_(bstack11ll11l111l_opy_):
    return bstack11l1l11_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨᩞ").format(bstack11lll1lll1l_opy_, bstack11ll11l111l_opy_)
def bstack1ll11ll11_opy_():
    return bstack111l1l1l11_opy_().replace(tzinfo=None).isoformat() + bstack11l1l11_opy_ (u"ࠪ࡞ࠬ᩟")
def bstack11ll1ll1ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11l1l11_opy_ (u"ࠫ࡟᩠࠭"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11l1l11_opy_ (u"ࠬࡠࠧᩡ")))).total_seconds() * 1000
def bstack11ll1ll11l1_opy_(timestamp):
    return bstack11ll1l111ll_opy_(timestamp).isoformat() + bstack11l1l11_opy_ (u"࡚࠭ࠨᩢ")
def bstack11ll111l1l1_opy_(bstack11lll111111_opy_):
    date_format = bstack11l1l11_opy_ (u"࡛ࠧࠦࠨࡱࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬᩣ")
    bstack11ll1ll11ll_opy_ = datetime.datetime.strptime(bstack11lll111111_opy_, date_format)
    return bstack11ll1ll11ll_opy_.isoformat() + bstack11l1l11_opy_ (u"ࠨ࡜ࠪᩤ")
def bstack11ll11l1l11_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11l1l11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᩥ")
    else:
        return bstack11l1l11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᩦ")
def bstack1ll11l1l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11l1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩᩧ")
def bstack11ll1111l11_opy_(val):
    return val.__str__().lower() == bstack11l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᩨ")
def bstack111ll1l1l1_opy_(bstack11ll11ll111_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11ll11ll111_opy_ as e:
                print(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨᩩ").format(func.__name__, bstack11ll11ll111_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1llll11l_opy_(bstack11ll11l1ll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11ll11l1ll1_opy_(cls, *args, **kwargs)
            except bstack11ll11ll111_opy_ as e:
                print(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡽࢀࠤ࠲ࡄࠠࡼࡿ࠽ࠤࢀࢃࠢᩪ").format(bstack11ll11l1ll1_opy_.__name__, bstack11ll11ll111_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1llll11l_opy_
    else:
        return decorator
def bstack1l1l1ll11l_opy_(bstack111l1111l1_opy_):
    if os.getenv(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫᩫ")) is not None:
        return bstack1ll11l1l1_opy_(os.getenv(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬᩬ")))
    if bstack11l1l11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᩭ") in bstack111l1111l1_opy_ and bstack11ll1111l11_opy_(bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᩮ")]):
        return False
    if bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᩯ") in bstack111l1111l1_opy_ and bstack11ll1111l11_opy_(bstack111l1111l1_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᩰ")]):
        return False
    return True
def bstack1lll1ll11l_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l1llll1l1_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠢᩱ"), None)
        return bstack11l1llll1l1_opy_ is None or bstack11l1llll1l1_opy_ == bstack11l1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠧᩲ")
    except Exception as e:
        return False
def bstack11111l1l_opy_(hub_url, CONFIG):
    if bstack1ll1lllll_opy_() <= version.parse(bstack11l1l11_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩᩳ")):
        if hub_url:
            return bstack11l1l11_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᩴ") + hub_url + bstack11l1l11_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣ᩵")
        return bstack11ll1ll1l1_opy_
    if hub_url:
        return bstack11l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢ᩶") + hub_url + bstack11l1l11_opy_ (u"ࠨ࠯ࡸࡦ࠲࡬ࡺࡨࠢ᩷")
    return bstack11ll1ll11_opy_
def bstack11ll1ll1111_opy_():
    return isinstance(os.getenv(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡍࡗࡊࡍࡓ࠭᩸")), str)
def bstack11l1ll1l1l_opy_(url):
    return urlparse(url).hostname
def bstack111111l1_opy_(hostname):
    for bstack111l11l11_opy_ in bstack1llll1ll11_opy_:
        regex = re.compile(bstack111l11l11_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11lll1l11l1_opy_(bstack11ll1ll111l_opy_, file_name, logger):
    bstack1l11l11ll_opy_ = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠨࢀࠪ᩹")), bstack11ll1ll111l_opy_)
    try:
        if not os.path.exists(bstack1l11l11ll_opy_):
            os.makedirs(bstack1l11l11ll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠩࢁࠫ᩺")), bstack11ll1ll111l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11l1l11_opy_ (u"ࠪࡻࠬ᩻")):
                pass
            with open(file_path, bstack11l1l11_opy_ (u"ࠦࡼ࠱ࠢ᩼")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l111ll1_opy_.format(str(e)))
def bstack11ll1l11111_opy_(file_name, key, value, logger):
    file_path = bstack11lll1l11l1_opy_(bstack11l1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᩽"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll1111_opy_ = json.load(open(file_path, bstack11l1l11_opy_ (u"࠭ࡲࡣࠩ᩾")))
        else:
            bstack1lll1111_opy_ = {}
        bstack1lll1111_opy_[key] = value
        with open(file_path, bstack11l1l11_opy_ (u"ࠢࡸ᩿࠭ࠥ")) as outfile:
            json.dump(bstack1lll1111_opy_, outfile)
def bstack1ll1l1llll_opy_(file_name, logger):
    file_path = bstack11lll1l11l1_opy_(bstack11l1l11_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᪀"), file_name, logger)
    bstack1lll1111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11l1l11_opy_ (u"ࠩࡵࠫ᪁")) as bstack1lll11lll_opy_:
            bstack1lll1111_opy_ = json.load(bstack1lll11lll_opy_)
    return bstack1lll1111_opy_
def bstack11lll11l11_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡪࡥ࡭ࡧࡷ࡭ࡳ࡭ࠠࡧ࡫࡯ࡩ࠿ࠦࠧ᪂") + file_path + bstack11l1l11_opy_ (u"ࠫࠥ࠭᪃") + str(e))
def bstack1ll1lllll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11l1l11_opy_ (u"ࠧࡂࡎࡐࡖࡖࡉ࡙ࡄࠢ᪄")
def bstack11l1l1l11l_opy_(config):
    if bstack11l1l11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᪅") in config:
        del (config[bstack11l1l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᪆")])
        return False
    if bstack1ll1lllll_opy_() < version.parse(bstack11l1l11_opy_ (u"ࠨ࠵࠱࠸࠳࠶ࠧ᪇")):
        return False
    if bstack1ll1lllll_opy_() >= version.parse(bstack11l1l11_opy_ (u"ࠩ࠷࠲࠶࠴࠵ࠨ᪈")):
        return True
    if bstack11l1l11_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ᪉") in config and config[bstack11l1l11_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᪊")] is False:
        return False
    else:
        return True
def bstack1llll11l11_opy_(args_list, bstack11ll1l1lll1_opy_):
    index = -1
    for value in bstack11ll1l1lll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11l11l1l11_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11l11l1l11_opy_ = bstack11l11l1l11_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11l1l11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᪋"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11l1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᪌"), exception=exception)
    def bstack1111ll1lll_opy_(self):
        if self.result != bstack11l1l11_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᪍"):
            return None
        if isinstance(self.exception_type, str) and bstack11l1l11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦ᪎") in self.exception_type:
            return bstack11l1l11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥ᪏")
        return bstack11l1l11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦ᪐")
    def bstack11lll111l11_opy_(self):
        if self.result != bstack11l1l11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ᪑"):
            return None
        if self.bstack11l11l1l11_opy_:
            return self.bstack11l11l1l11_opy_
        return bstack11ll1l111l1_opy_(self.exception)
def bstack11ll1l111l1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll11l11l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llllllll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack11lll1lll_opy_(config, logger):
    try:
        import playwright
        bstack11ll1l1llll_opy_ = playwright.__file__
        bstack11ll111l11l_opy_ = os.path.split(bstack11ll1l1llll_opy_)
        bstack11ll1lll1l1_opy_ = bstack11ll111l11l_opy_[0] + bstack11l1l11_opy_ (u"ࠬ࠵ࡤࡳ࡫ࡹࡩࡷ࠵ࡰࡢࡥ࡮ࡥ࡬࡫࠯࡭࡫ࡥ࠳ࡨࡲࡩ࠰ࡥ࡯࡭࠳ࡰࡳࠨ᪒")
        os.environ[bstack11l1l11_opy_ (u"࠭ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠩ᪓")] = bstack11ll1l1l1_opy_(config)
        with open(bstack11ll1lll1l1_opy_, bstack11l1l11_opy_ (u"ࠧࡳࠩ᪔")) as f:
            bstack1lllllllll_opy_ = f.read()
            bstack11ll11l1111_opy_ = bstack11l1l11_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠧ᪕")
            bstack11ll1111l1l_opy_ = bstack1lllllllll_opy_.find(bstack11ll11l1111_opy_)
            if bstack11ll1111l1l_opy_ == -1:
              process = subprocess.Popen(bstack11l1l11_opy_ (u"ࠤࡱࡴࡲࠦࡩ࡯ࡵࡷࡥࡱࡲࠠࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹࠨ᪖"), shell=True, cwd=bstack11ll111l11l_opy_[0])
              process.wait()
              bstack11ll1l1l1ll_opy_ = bstack11l1l11_opy_ (u"ࠪࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴࠣ࠽ࠪ᪗")
              bstack11lll1l1l1l_opy_ = bstack11l1l11_opy_ (u"ࠦࠧࠨࠠ࡝ࠤࡸࡷࡪࠦࡳࡵࡴ࡬ࡧࡹࡢࠢ࠼ࠢࡦࡳࡳࡹࡴࠡࡽࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵࠦࡽࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫ࠮ࡁࠠࡪࡨࠣࠬࡵࡸ࡯ࡤࡧࡶࡷ࠳࡫࡮ࡷ࠰ࡊࡐࡔࡈࡁࡍࡡࡄࡋࡊࡔࡔࡠࡊࡗࡘࡕࡥࡐࡓࡑ࡛࡝࠮ࠦࡢࡰࡱࡷࡷࡹࡸࡡࡱࠪࠬ࠿ࠥࠨࠢࠣ᪘")
              bstack11lll1111l1_opy_ = bstack1lllllllll_opy_.replace(bstack11ll1l1l1ll_opy_, bstack11lll1l1l1l_opy_)
              with open(bstack11ll1lll1l1_opy_, bstack11l1l11_opy_ (u"ࠬࡽࠧ᪙")) as f:
                f.write(bstack11lll1111l1_opy_)
    except Exception as e:
        logger.error(bstack111l1llll_opy_.format(str(e)))
def bstack1l11l1llll_opy_():
  try:
    bstack11lll111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬࠯࡬ࡶࡳࡳ࠭᪚"))
    bstack11lll11l111_opy_ = []
    if os.path.exists(bstack11lll111lll_opy_):
      with open(bstack11lll111lll_opy_) as f:
        bstack11lll11l111_opy_ = json.load(f)
      os.remove(bstack11lll111lll_opy_)
    return bstack11lll11l111_opy_
  except:
    pass
  return []
def bstack1l11llll_opy_(bstack1l11ll1111_opy_):
  try:
    bstack11lll11l111_opy_ = []
    bstack11lll111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧ᪛"))
    if os.path.exists(bstack11lll111lll_opy_):
      with open(bstack11lll111lll_opy_) as f:
        bstack11lll11l111_opy_ = json.load(f)
    bstack11lll11l111_opy_.append(bstack1l11ll1111_opy_)
    with open(bstack11lll111lll_opy_, bstack11l1l11_opy_ (u"ࠨࡹࠪ᪜")) as f:
        json.dump(bstack11lll11l111_opy_, f)
  except:
    pass
def bstack1l111lll1_opy_(logger, bstack11ll1ll1l11_opy_ = False):
  try:
    test_name = os.environ.get(bstack11l1l11_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬ᪝"), bstack11l1l11_opy_ (u"ࠪࠫ᪞"))
    if test_name == bstack11l1l11_opy_ (u"ࠫࠬ᪟"):
        test_name = threading.current_thread().__dict__.get(bstack11l1l11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡇࡪࡤࡠࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫ᪠"), bstack11l1l11_opy_ (u"࠭ࠧ᪡"))
    bstack11l1llllll1_opy_ = bstack11l1l11_opy_ (u"ࠧ࠭ࠢࠪ᪢").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll1ll1l11_opy_:
        bstack1l1l1l111_opy_ = os.environ.get(bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᪣"), bstack11l1l11_opy_ (u"ࠩ࠳ࠫ᪤"))
        bstack11ll111ll1_opy_ = {bstack11l1l11_opy_ (u"ࠪࡲࡦࡳࡥࠨ᪥"): test_name, bstack11l1l11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᪦"): bstack11l1llllll1_opy_, bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᪧ"): bstack1l1l1l111_opy_}
        bstack11ll1l11l11_opy_ = []
        bstack11ll1111111_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡰࡱࡲࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ᪨"))
        if os.path.exists(bstack11ll1111111_opy_):
            with open(bstack11ll1111111_opy_) as f:
                bstack11ll1l11l11_opy_ = json.load(f)
        bstack11ll1l11l11_opy_.append(bstack11ll111ll1_opy_)
        with open(bstack11ll1111111_opy_, bstack11l1l11_opy_ (u"ࠧࡸࠩ᪩")) as f:
            json.dump(bstack11ll1l11l11_opy_, f)
    else:
        bstack11ll111ll1_opy_ = {bstack11l1l11_opy_ (u"ࠨࡰࡤࡱࡪ࠭᪪"): test_name, bstack11l1l11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᪫"): bstack11l1llllll1_opy_, bstack11l1l11_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ᪬"): str(multiprocessing.current_process().name)}
        if bstack11l1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ᪭") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack11ll111ll1_opy_)
  except Exception as e:
      logger.warn(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ᪮").format(e))
def bstack1l1ll111ll_opy_(error_message, test_name, index, logger):
  try:
    bstack11lll1111ll_opy_ = []
    bstack11ll111ll1_opy_ = {bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᪯"): test_name, bstack11l1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᪰"): error_message, bstack11l1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ᪱"): index}
    bstack11ll111llll_opy_ = os.path.join(tempfile.gettempdir(), bstack11l1l11_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ᪲"))
    if os.path.exists(bstack11ll111llll_opy_):
        with open(bstack11ll111llll_opy_) as f:
            bstack11lll1111ll_opy_ = json.load(f)
    bstack11lll1111ll_opy_.append(bstack11ll111ll1_opy_)
    with open(bstack11ll111llll_opy_, bstack11l1l11_opy_ (u"ࠪࡻࠬ᪳")) as f:
        json.dump(bstack11lll1111ll_opy_, f)
  except Exception as e:
    logger.warn(bstack11l1l11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡶࡲࡶࡪࠦࡲࡰࡤࡲࡸࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ᪴").format(e))
def bstack1111llll1_opy_(bstack11lll11ll_opy_, name, logger):
  try:
    bstack11ll111ll1_opy_ = {bstack11l1l11_opy_ (u"ࠬࡴࡡ࡮ࡧ᪵ࠪ"): name, bstack11l1l11_opy_ (u"࠭ࡥࡳࡴࡲࡶ᪶ࠬ"): bstack11lll11ll_opy_, bstack11l1l11_opy_ (u"ࠧࡪࡰࡧࡩࡽ᪷࠭"): str(threading.current_thread()._name)}
    return bstack11ll111ll1_opy_
  except Exception as e:
    logger.warn(bstack11l1l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡦࡪ࡮ࡡࡷࡧࠣࡪࡺࡴ࡮ࡦ࡮ࠣࡨࡦࡺࡡ࠻ࠢࡾࢁ᪸ࠧ").format(e))
  return
def bstack11lll1l11ll_opy_():
    return platform.system() == bstack11l1l11_opy_ (u"࡚ࠩ࡭ࡳࡪ࡯ࡸࡵ᪹ࠪ")
def bstack1ll1l11l_opy_(bstack11ll111l111_opy_, config, logger):
    bstack11ll11lllll_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11ll111l111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡦࡪ࡮ࡷࡩࡷࠦࡣࡰࡰࡩ࡭࡬ࠦ࡫ࡦࡻࡶࠤࡧࡿࠠࡳࡧࡪࡩࡽࠦ࡭ࡢࡶࡦ࡬࠿ࠦࡻࡾࠤ᪺").format(e))
    return bstack11ll11lllll_opy_
def bstack11lll11llll_opy_(bstack11l1lllllll_opy_, bstack11lll11l11l_opy_):
    bstack11lll1ll1l1_opy_ = version.parse(bstack11l1lllllll_opy_)
    bstack11ll1ll1lll_opy_ = version.parse(bstack11lll11l11l_opy_)
    if bstack11lll1ll1l1_opy_ > bstack11ll1ll1lll_opy_:
        return 1
    elif bstack11lll1ll1l1_opy_ < bstack11ll1ll1lll_opy_:
        return -1
    else:
        return 0
def bstack111l1l1l11_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll1l111ll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11ll111l1ll_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11ll1l1l_opy_(options, framework, bstack11l1l111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11l1l11_opy_ (u"ࠫ࡬࡫ࡴࠨ᪻"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11l11ll1_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᪼"))
    bstack11ll11111ll_opy_ = True
    bstack1l11l1111_opy_ = os.environ[bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇ᪽ࠫ")]
    if bstack11ll1111l11_opy_(caps.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭᪾"))) or bstack11ll1111l11_opy_(caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᪿ"))):
        bstack11ll11111ll_opy_ = False
    if bstack11l1l1l11l_opy_({bstack11l1l11_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤᫀ"): bstack11ll11111ll_opy_}):
        bstack11l11ll1_opy_ = bstack11l11ll1_opy_ or {}
        bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᫁")] = bstack11ll111l1ll_opy_(framework)
        bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᫂")] = bstack1ll1111l1ll_opy_()
        bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᫃")] = bstack1l11l1111_opy_
        bstack11l11ll1_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᫄")] = bstack11l1l111l_opy_
        if getattr(options, bstack11l1l11_opy_ (u"ࠧࡴࡧࡷࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡹࠨ᫅"), None):
            options.set_capability(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᫆"), bstack11l11ll1_opy_)
        else:
            options[bstack11l1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᫇")] = bstack11l11ll1_opy_
    else:
        if getattr(options, bstack11l1l11_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫ᫈"), None):
            options.set_capability(bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᫉"), bstack11ll111l1ll_opy_(framework))
            options.set_capability(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ᫊࠭"), bstack1ll1111l1ll_opy_())
            options.set_capability(bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᫋"), bstack1l11l1111_opy_)
            options.set_capability(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᫌ"), bstack11l1l111l_opy_)
        else:
            options[bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᫍ")] = bstack11ll111l1ll_opy_(framework)
            options[bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᫎ")] = bstack1ll1111l1ll_opy_()
            options[bstack11l1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡷࡩࡸࡺࡨࡶࡤࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᫏")] = bstack1l11l1111_opy_
            options[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᫐")] = bstack11l1l111l_opy_
    return options
def bstack11ll11lll11_opy_(bstack11lll1l111l_opy_, framework):
    bstack11l1l111l_opy_ = bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠧࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡓࡖࡔࡊࡕࡄࡖࡢࡑࡆࡖࠢ᫑"))
    if bstack11lll1l111l_opy_ and len(bstack11lll1l111l_opy_.split(bstack11l1l11_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬ᫒"))) > 1:
        ws_url = bstack11lll1l111l_opy_.split(bstack11l1l11_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭᫓"))[0]
        if bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ᫔") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1lllll1l_opy_ = json.loads(urllib.parse.unquote(bstack11lll1l111l_opy_.split(bstack11l1l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᫕"))[1]))
            bstack11l1lllll1l_opy_ = bstack11l1lllll1l_opy_ or {}
            bstack1l11l1111_opy_ = os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᫖")]
            bstack11l1lllll1l_opy_[bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬ᫗")] = str(framework) + str(__version__)
            bstack11l1lllll1l_opy_[bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᫘")] = bstack1ll1111l1ll_opy_()
            bstack11l1lllll1l_opy_[bstack11l1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡺࡥࡴࡶ࡫ࡹࡧࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᫙")] = bstack1l11l1111_opy_
            bstack11l1lllll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᫚")] = bstack11l1l111l_opy_
            bstack11lll1l111l_opy_ = bstack11lll1l111l_opy_.split(bstack11l1l11_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᫛"))[0] + bstack11l1l11_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᫜") + urllib.parse.quote(json.dumps(bstack11l1lllll1l_opy_))
    return bstack11lll1l111l_opy_
def bstack1lll1l1l1l_opy_():
    global bstack1l1l11l11_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l11l11_opy_ = BrowserType.connect
    return bstack1l1l11l11_opy_
def bstack11lllll1l_opy_(framework_name):
    global bstack1l11lll1l_opy_
    bstack1l11lll1l_opy_ = framework_name
    return framework_name
def bstack11llll111_opy_(self, *args, **kwargs):
    global bstack1l1l11l11_opy_
    try:
        global bstack1l11lll1l_opy_
        if bstack11l1l11_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧ᫝") in kwargs:
            kwargs[bstack11l1l11_opy_ (u"ࠫࡼࡹࡅ࡯ࡦࡳࡳ࡮ࡴࡴࠨ᫞")] = bstack11ll11lll11_opy_(
                kwargs.get(bstack11l1l11_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩ᫟"), None),
                bstack1l11lll1l_opy_
            )
    except Exception as e:
        logger.error(bstack11l1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡔࡆࡎࠤࡨࡧࡰࡴ࠼ࠣࡿࢂࠨ᫠").format(str(e)))
    return bstack1l1l11l11_opy_(self, *args, **kwargs)
def bstack11ll111111l_opy_(bstack11ll11l1l1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1ll11lll1_opy_(bstack11ll11l1l1l_opy_, bstack11l1l11_opy_ (u"ࠢࠣ᫡"))
        if proxies and proxies.get(bstack11l1l11_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ᫢")):
            parsed_url = urlparse(proxies.get(bstack11l1l11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᫣")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11l1l11_opy_ (u"ࠪࡴࡷࡵࡸࡺࡊࡲࡷࡹ࠭᫤")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11l1l11_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡳࡷࡺࠧ᫥")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11l1l11_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨ᫦")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11l1l11_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩ᫧")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1l111ll1_opy_(bstack11ll11l1l1l_opy_):
    bstack11l1lllll11_opy_ = {
        bstack11lll1llll1_opy_[bstack11lll111l1l_opy_]: bstack11ll11l1l1l_opy_[bstack11lll111l1l_opy_]
        for bstack11lll111l1l_opy_ in bstack11ll11l1l1l_opy_
        if bstack11lll111l1l_opy_ in bstack11lll1llll1_opy_
    }
    bstack11l1lllll11_opy_[bstack11l1l11_opy_ (u"ࠢࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠢ᫨")] = bstack11ll111111l_opy_(bstack11ll11l1l1l_opy_, bstack111ll1lll_opy_.get_property(bstack11l1l11_opy_ (u"ࠣࡲࡵࡳࡽࡿࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠣ᫩")))
    bstack11ll11ll1l1_opy_ = [element.lower() for element in bstack11llll1ll11_opy_]
    bstack11ll1111lll_opy_(bstack11l1lllll11_opy_, bstack11ll11ll1l1_opy_)
    return bstack11l1lllll11_opy_
def bstack11ll1111lll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11l1l11_opy_ (u"ࠤ࠭࠮࠯࠰ࠢ᫪")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll1111lll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll1111lll_opy_(item, keys)
def bstack11lll1ll11l_opy_():
    bstack11ll111ll1l_opy_ = [os.environ.get(bstack11l1l11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡍࡑࡋࡓࡠࡆࡌࡖࠧ᫫")), os.path.join(os.path.expanduser(bstack11l1l11_opy_ (u"ࠦࢃࠨ᫬")), bstack11l1l11_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ᫭")), os.path.join(bstack11l1l11_opy_ (u"࠭࠯ࡵ࡯ࡳࠫ᫮"), bstack11l1l11_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ᫯"))]
    for path in bstack11ll111ll1l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11l1l11_opy_ (u"ࠣࡈ࡬ࡰࡪࠦࠧࠣ᫰") + str(path) + bstack11l1l11_opy_ (u"ࠤࠪࠤࡪࡾࡩࡴࡶࡶ࠲ࠧ᫱"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11l1l11_opy_ (u"ࠥࡋ࡮ࡼࡩ࡯ࡩࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠡࡨࡲࡶࠥ࠭ࠢ᫲") + str(path) + bstack11l1l11_opy_ (u"ࠦࠬࠨ᫳"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11l1l11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࠫࠧ᫴") + str(path) + bstack11l1l11_opy_ (u"ࠨࠧࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡸࠦࡴࡩࡧࠣࡶࡪࡷࡵࡪࡴࡨࡨࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵ࠱ࠦ᫵"))
            else:
                logger.debug(bstack11l1l11_opy_ (u"ࠢࡄࡴࡨࡥࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫ࠠࠨࠤ᫶") + str(path) + bstack11l1l11_opy_ (u"ࠣࠩࠣࡻ࡮ࡺࡨࠡࡹࡵ࡭ࡹ࡫ࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱ࠲ࠧ᫷"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11l1l11_opy_ (u"ࠤࡒࡴࡪࡸࡡࡵ࡫ࡲࡲࠥࡹࡵࡤࡥࡨࡩࡩ࡫ࡤࠡࡨࡲࡶࠥ࠭ࠢ᫸") + str(path) + bstack11l1l11_opy_ (u"ࠥࠫ࠳ࠨ᫹"))
            return path
        except Exception as e:
            logger.debug(bstack11l1l11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡺࡶࠠࡧ࡫࡯ࡩࠥ࠭ࡻࡱࡣࡷ࡬ࢂ࠭࠺ࠡࠤ᫺") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨ᫻"))
    logger.debug(bstack11l1l11_opy_ (u"ࠨࡁ࡭࡮ࠣࡴࡦࡺࡨࡴࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠥ᫼"))
    return None
@measure(event_name=EVENTS.bstack11llll111ll_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
def bstack1llllll1l11_opy_(binary_path, bstack1llllll1111_opy_, bs_config):
    logger.debug(bstack11l1l11_opy_ (u"ࠢࡄࡷࡵࡶࡪࡴࡴࠡࡅࡏࡍࠥࡖࡡࡵࡪࠣࡪࡴࡻ࡮ࡥ࠼ࠣࡿࢂࠨ᫽").format(binary_path))
    bstack11ll1l11ll1_opy_ = bstack11l1l11_opy_ (u"ࠨࠩ᫾")
    bstack11ll11llll1_opy_ = {
        bstack11l1l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᫿"): __version__,
        bstack11l1l11_opy_ (u"ࠥࡳࡸࠨᬀ"): platform.system(),
        bstack11l1l11_opy_ (u"ࠦࡴࡹ࡟ࡢࡴࡦ࡬ࠧᬁ"): platform.machine(),
        bstack11l1l11_opy_ (u"ࠧࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠥᬂ"): bstack11l1l11_opy_ (u"࠭࠰ࠨᬃ"),
        bstack11l1l11_opy_ (u"ࠢࡴࡦ࡮ࡣࡱࡧ࡮ࡨࡷࡤ࡫ࡪࠨᬄ"): bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᬅ")
    }
    try:
        if binary_path:
            bstack11ll11llll1_opy_[bstack11l1l11_opy_ (u"ࠩࡦࡰ࡮ࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᬆ")] = subprocess.check_output([binary_path, bstack11l1l11_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᬇ")]).strip().decode(bstack11l1l11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᬈ"))
        response = requests.request(
            bstack11l1l11_opy_ (u"ࠬࡍࡅࡕࠩᬉ"),
            url=bstack1ll11l11l_opy_(bstack11llll11lll_opy_),
            headers=None,
            auth=(bs_config[bstack11l1l11_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨᬊ")], bs_config[bstack11l1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪᬋ")]),
            json=None,
            params=bstack11ll11llll1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11l1l11_opy_ (u"ࠨࡷࡵࡰࠬᬌ") in data.keys() and bstack11l1l11_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦࡢࡧࡱ࡯࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᬍ") in data.keys():
            logger.debug(bstack11l1l11_opy_ (u"ࠥࡒࡪ࡫ࡤࠡࡶࡲࠤࡺࡶࡤࡢࡶࡨࠤࡧ࡯࡮ࡢࡴࡼ࠰ࠥࡩࡵࡳࡴࡨࡲࡹࠦࡢࡪࡰࡤࡶࡾࠦࡶࡦࡴࡶ࡭ࡴࡴ࠺ࠡࡽࢀࠦᬎ").format(bstack11ll11llll1_opy_[bstack11l1l11_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᬏ")]))
            bstack11l1llll111_opy_ = bstack11ll11l11ll_opy_(data[bstack11l1l11_opy_ (u"ࠬࡻࡲ࡭ࠩᬐ")], bstack1llllll1111_opy_)
            bstack11ll1l11ll1_opy_ = os.path.join(bstack1llllll1111_opy_, bstack11l1llll111_opy_)
            os.chmod(bstack11ll1l11ll1_opy_, 0o777) # bstack11lll1l1lll_opy_ permission
            return bstack11ll1l11ll1_opy_
    except Exception as e:
        logger.debug(bstack11l1l11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡩࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡱࡩࡼࠦࡓࡅࡍࠣࡿࢂࠨᬑ").format(e))
    return binary_path
@measure(event_name=EVENTS.bstack11llll1l1l1_opy_, stage=STAGE.bstack1l1ll1lll_opy_)
def bstack11ll11l11ll_opy_(bstack11ll1lllll1_opy_, bstack11ll1l11l1l_opy_):
    logger.debug(bstack11l1l11_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤᬒ") + str(bstack11ll1lllll1_opy_) + bstack11l1l11_opy_ (u"ࠣࠤᬓ"))
    zip_path = os.path.join(bstack11ll1l11l1l_opy_, bstack11l1l11_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣᬔ"))
    bstack11l1llll111_opy_ = bstack11l1l11_opy_ (u"ࠪࠫᬕ")
    with requests.get(bstack11ll1lllll1_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11l1l11_opy_ (u"ࠦࡼࡨࠢᬖ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11l1l11_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢᬗ"))
    with zipfile.ZipFile(zip_path, bstack11l1l11_opy_ (u"࠭ࡲࠨᬘ")) as zip_ref:
        bstack11lll1l1111_opy_ = zip_ref.namelist()
        if len(bstack11lll1l1111_opy_) > 0:
            bstack11l1llll111_opy_ = bstack11lll1l1111_opy_[0] # bstack11lll11ll1l_opy_ bstack11llll1l1ll_opy_ will be bstack11ll1l1l11l_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11ll1l11l1l_opy_)
        logger.debug(bstack11l1l11_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨᬙ") + str(bstack11ll1l11l1l_opy_) + bstack11l1l11_opy_ (u"ࠣࠩࠥᬚ"))
    os.remove(zip_path)
    return bstack11l1llll111_opy_
def get_cli_dir():
    bstack11lll11l1l1_opy_ = bstack11lll1ll11l_opy_()
    if bstack11lll11l1l1_opy_:
        bstack1llllll1111_opy_ = os.path.join(bstack11lll11l1l1_opy_, bstack11l1l11_opy_ (u"ࠤࡦࡰ࡮ࠨᬛ"))
        if not os.path.exists(bstack1llllll1111_opy_):
            os.makedirs(bstack1llllll1111_opy_, mode=0o777, exist_ok=True)
        return bstack1llllll1111_opy_
    else:
        raise FileNotFoundError(bstack11l1l11_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨᬜ"))
def bstack1lll111ll1l_opy_(bstack1llllll1111_opy_):
    bstack11l1l11_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣᬝ")
    bstack11lll11ll11_opy_ = [
        os.path.join(bstack1llllll1111_opy_, f)
        for f in os.listdir(bstack1llllll1111_opy_)
        if os.path.isfile(os.path.join(bstack1llllll1111_opy_, f)) and f.startswith(bstack11l1l11_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨᬞ"))
    ]
    if len(bstack11lll11ll11_opy_) > 0:
        return max(bstack11lll11ll11_opy_, key=os.path.getmtime) # get bstack11ll1l1l111_opy_ binary
    return bstack11l1l11_opy_ (u"ࠨࠢᬟ")