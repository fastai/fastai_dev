# fastai Link Checker

This is https://github.com/w3c/link-checker with some custom tweaks.

## Prerequisites

```
sudo apt install w3c-linkchecker
```

## Usage

Note, that if you have just committed changes to git, wait a few minutes for github pages to sync, otherwise you'll be testing an outdated live site.

Test docs*.fast.ai for broken links and anchors:

```
cd checklink
./checklink-docs.sh
./checklink-docs-dev.sh
```

Each file logs to console and also into `checklink-docs.log` and `checklink-docs-dev.log`

If you're on windows w/o bash and assuming you have [perl installed](https://learn.perl.org/installing/windows.html), you can run it directly like:

```
perl fastai-checklink --depth 50 --quiet --broken -e --sleep 2 --timeout 60 --connection-cache 3 --exclude github.com --exclude test.pypi.org --exclude ycombinator.com --exclude anaconda.org --exclude google.com --cookies cookies.txt "https://docs.fast.ai"
```

The script is set to sleep for 2 secs between each request, so not to get blocked by github, so it takes some 5-10min to complete.

You can add `--html` inside those scripts if you prefer to have the html output (in which case change the scripts to `|tee checklink-docs-log.html` or similar, since it dumps the output to stdout.

## Checking the site locally:

XXX: After we make the real filenames and the links consistent (i.e. either both using .html or both not) we can then do a much faster test on the local system:

```
fastai-checklink --masquerade "/ https://docs.fast.ai/" docs
```

## More on Prerequisites

If for any reason you don't have the apt packages for `w3c-linkchecker`, you can install those manually with:

```
sudo apt install cpanminus
sudo cpanm W3C::LinkChecker
```

or via CPAN shell:

```
apt install cpanplus
perl -MCPAN -e shell
install install W3C::LinkChecker
```

and now you can invoke `./checklink`.


## Portable sript

You can ignore the rest of this document, unless you'd like to build a perl executable with all the prerequisites built in. It's not part of the repo because of its significant size.

## Building the executable

If for any reason you need to create an executable (or make one for another platform), install the script's dependencies (previous step), the build tools and then make the executable.

## Build tools prerequisites

Install Perl PAR Packager:

```
sudo apt install libpar-packer-perl
```

or via cpanm:

```
cpanm pp
```

or via CPAN shell:

```
perl -MCPAN -e shell
install pp
```

## Build the portable version of the tool

This will build a portable executable version for your platform (it's portable in a sense that it doesn't need any of its many dependencies). e.g. for linux:

```
cd checklink
pp -o checklink-linux checklink
```
