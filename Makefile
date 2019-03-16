.PHONY: strip git-clean-nb_dirs-check

nb_dirs = dev_nb dev_course

git-clean-nb_dirs-check:
	@echo "\n\n*** Checking that everything under nb_dirs is committed"
	@if [ -n "$(shell git status -s $(nb_dirs))" ]; then\
		echo "git status $(nb_dirs) is not clean. You have uncommitted git files";\
		exit 1;\
	else\
		echo "git status $(nb_dirs) is clean";\
    fi

strip: git-clean-nb_dirs-check
	@echo "Stripping out nbs"
	tools/trust-origin-git-config -d
	git pull
	tools/fastai-nbstripout -d dev_nb/*ipynb dev_nb/experiments/*ipynb dev_course/*/*ipynb
	git commit -m "strip out nbs" $(nb_dirs)
	git push
	tools/trust-origin-git-config -e
