.PHONY: strip git-clean-nb_dirs-check

nb_dirs = dev_nb dev_course dev_swift

git-clean-nb_dirs-check:
	@echo "\n\n*** Checking that everything under '$(nb_dirs)' is committed"
	@if [ -n "$(shell git status -s $(nb_dirs))" ]; then\
		echo "git status $(nb_dirs) is not clean. You have uncommitted git files (use git stash or git commit)";\
		exit 1;\
	else\
		echo "git status $(nb_dirs) is clean";\
    fi

strip: # strip out nbs, that were committed unstripped out, and commit+push
	${MAKE} strip-try; \
	${MAKE} strip-finally

strip-finally: # restore .gitconfig
	tools/trust-origin-git-config -e

strip-try: git-clean-nb_dirs-check # try to strip out && commit
	@echo "Stripping out nbs"
	tools/trust-origin-git-config -d
	git pull
	tools/fastai-nbstripout dev_nb/*ipynb dev_nb/experiments/*ipynb
	tools/fastai-nbstripout -d dev_course/*/*ipynb dev_swift/*ipynb
	git commit -m "strip out nbs" $(nb_dirs)
	git push
