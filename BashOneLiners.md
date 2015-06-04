Pack a file or folder to tar.gz showing progress with [pv](http://www.ivarch.com/programs/pv.shtml)
```
x=target-file-or-dir; du -sh $x && tar cf - $x | pv -s $(du -sb $x | awk '{print \$1}') | gzip > $x.tar.gz && du -sh $x.tar.gz
```