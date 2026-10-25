#!/usr/bin/env python3
"""Safe extraction for pinned archives; caller supplies a new empty staging directory."""
import argparse
import copy
from pathlib import Path, PurePosixPath
import shutil
import stat
import tarfile
import zipfile

def name(value, strip):
    path=PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '\\' in value or ':' in value:
        raise ValueError('Unsafe archive path: '+value)
    return PurePosixPath(*path.parts[strip:]).as_posix() if len(path.parts)>strip else None

def extract(archive, destination, strip=0):
    if destination.is_symlink() or destination.resolve()!=destination.absolute() or not destination.is_dir() or list(destination.iterdir()):
        raise ValueError('Extraction requires a new empty directory')
    if strip<0:raise ValueError('strip must be nonnegative')
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as source:
            entries=[]; seen=set()
            for entry in source.infolist():
                relative=name(entry.filename,strip)
                mode=entry.external_attr>>16
                if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0,stat.S_IFREG,stat.S_IFDIR)):
                    raise ValueError('Unsupported ZIP entry: '+entry.filename)
                if relative and relative in seen and not entry.is_dir():raise ValueError('Duplicate ZIP path')
                if relative:seen.add(relative);entries.append((entry,relative))
            for entry,relative in entries:
                target=destination/relative
                if entry.is_dir():target.mkdir(parents=True,exist_ok=True);continue
                target.parent.mkdir(parents=True,exist_ok=True)
                with source.open(entry) as stream,target.open('xb') as output:shutil.copyfileobj(stream,output)
                target.chmod((mode&0o755) or 0o644)
    else:
        if not hasattr(tarfile,'data_filter'):raise ValueError('Python with tarfile.data_filter required (3.12+, or patched 3.11)')
        with tarfile.open(archive) as source:
            entries=[]
            for entry in source.getmembers():
                relative=name(entry.name,strip)
                if not relative:continue
                item=copy.copy(entry);item.name=relative
                if item.islnk():
                    item.linkname=name(item.linkname,strip)
                    if not item.linkname:raise ValueError('Invalid stripped hardlink')
                # data_filter checks symlink/hardlink resolution against destination too.
                tarfile.data_filter(item,str(destination))
                entries.append(item)
            source.extractall(destination,members=entries,filter='data')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('archive',type=Path);ap.add_argument('destination',type=Path);ap.add_argument('--strip',type=int,default=0)
    args=ap.parse_args();extract(args.archive,args.destination,args.strip)
if __name__=='__main__':main()
