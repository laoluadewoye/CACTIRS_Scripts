#!/usr/bin/env python

from mpi4py import MPI
import gdisplayMod

comm = MPI.COMM_WORLD

paragraph = "Love isn't always a ray of sunshine. That's what the older girls kept telling her when she said she had found the perfect man. She had thought this was simply bitter talk on their part since they had been unable to find true love like hers. But now she had to face the fact that they may have been right. Love may not always be a ray of sunshine. That is unless they were referring to how the sun can burn."

print ("\n Static paragraph box:")

newParagraph = gdisplayMod.splitPara(paragraph, 50)
gdisplayMod.graphicsMultiline(newParagraph)

print ("\n\n Dynamic paragraph box:")

dynamicParagraph = gdisplayMod.splitParaDynamic(paragraph)
gdisplayMod.graphicsMultiline(dynamicParagraph)
