import os
import tarfile
import json

import spicedham as sh
print 'extracting'
tarball = 'corpus_20140729.tar.gz'
if os.path.exists('corpus'):
    os.system('rm -rf corpus')
tar = tarfile.open(tarball)
tar.extractall()
tar.close()
print 'making dirs'
os.chdir('corpus')
os.mkdir(os.path.join('train'))
os.mkdir(os.path.join('train/spam'))
os.mkdir(os.path.join('train/ham'))
os.mkdir(os.path.join('control'))
os.mkdir(os.path.join('control/spam'))
os.mkdir(os.path.join('control/ham'))

print 'sorting corpus ham'

for f in zip(os.listdir('ham'), range(len(os.listdir('ham')))):
    if f[1] % 2 == 0:
        os.rename(os.path.join('ham',  f[0]), os.path.join('control', 'ham', f[0]))
    else:
        os.rename(os.path.join('ham',  f[0]), os.path.join('train', 'ham', f[0]))
 
print 'sorting corpus spam'
for f in zip(os.listdir('spam'), range(len(os.listdir('spam')))):
    if f[1] % 2 == 0:
        os.rename(os.path.join('spam',  f[0]), os.path.join('control', 'spam', f[0]))
    else:
        os.rename(os.path.join('spam',  f[0]), os.path.join('train', 'spam', f[0]))

os.chdir('..')
print 'make object'
Sh = sh.SpicedHam()
print 'training spam'
for f in os.listdir(os.path.join('corpus', 'train', 'spam')):
    ff = open('corpus/train/spam/' + f, 'r')
    Sh.train(json.load(ff), True)
        
print 'training ham'
for f in os.listdir(os.path.join('corpus', 'train', 'ham')):
    ff = open('corpus/train/ham/' + f, 'r')
    Sh.train(json.load(ff), False)


numSpamWarnings = 0
numHamWarnings = 0
numSpamFail = 0
numHamFail = 0

print 'checking spam messages'
numSpamMessages = len(os.listdir('corpus/train/spam'))
for fname in os.listdir('corpus/train/spam'):
    f = open('corpus/train/spam/' + fname, 'r')
    ps = Sh.is_spam(json.load(f))
    if 0.0 < round(ps, 3) > 1.0:
        print "\033[0;91mFAIL\033[0m " + str(ps)
        numSpamFail += 1
        print 'corpus/train/spam/' + fname
    elif ps <  0.5:
        print "\033[;91mWARN\033[0m"
        print 'corpus/train/spam/' + fname
        numSpamWarnings += 1
    #else:
    #    print 'success ' + str(ps)

print '\t\t\t\t\tchecking a ham messages'
numHamMessages = len(os.listdir('corpus/train/ham'))
for fname in os.listdir('corpus/train/ham'):
    f = open('corpus/train/ham/' + fname, 'r')
    ps = Sh.is_spam(json.load(f))
    if 0.0 < round(ps, 3) > 1.0:
        print "\033[0;91mFAIL\033[0m " + str(ps)
        numHamFail += 1
        print 'corpus/train/ham/' + fname
    elif ps >  0.5:
        print "\033[;91mWARN\033[0m" + str(ps)
        print 'corpus/train/ham/' + fname
        numHamWarnings += 1
    #else:
#    print 'success ' + str(ps)
print 'processed {} messages'.format(numSpamMessages + numHamMessages)
print 'True positives {}'.format(numSpamMessages - numSpamWarnings)
print 'False positives {}'.format(numHamWarnings)
print 'True negatives {}'.format(numHamMessages - numHamWarnings)
print 'False negatives {}'.format(numSpamWarnings)
print 'There were {} failures, {} spam, {} ham'.format(numSpamFail + numHamFail, numSpamFail, numHamFail)
