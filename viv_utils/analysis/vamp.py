import logging
import binascii

from viv_utils import make_library_function
from viv_utils.analysis.sigs.msvc.vc32rtf import sigs as sigs_vc32rtf

import envi.bytesig as e_bytesig


logger = logging.getLogger(__name__)


class VampSignatures(e_bytesig.SignatureTree):
    def __init__(self):
        logger.debug("loading %d signatures" % len(sigs_vc32rtf))
        e_bytesig.SignatureTree.__init__(self)
        for bytez, masks, fname in sigs_vc32rtf:
            bytez = binascii.unhexlify(bytez)
            if masks is not None:
                masks = binascii.unhexlify(masks)
            self.addSignature(bytez, masks=masks, val=fname)


vs = VampSignatures()


def analyzeFunction(vw, funcva):
    offset, bytes = vw.getByteDef(funcva)
    sig = vs.getSignature(bytes, offset)
    if sig is not None:
        fname = sig.split(".")[-1]
        vw.makeName(funcva, "%s_%.8x" % (fname, funcva), filelocal=True)
        make_library_function(vw, funcva)
        logger.debug("0x%X identified library function %s", funcva, fname)
