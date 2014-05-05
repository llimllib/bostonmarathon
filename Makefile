notebook:
	ipython notebook --notebook-dir=.

serve:
	python -m SimpleHTTPServer

push:
	-git branch -D gh-pages
	git checkout --orphan gh-pages
	git rm -rf .
	git checkout master -- index.md maps
	# pip install grip
	grip index.md --export
	git add index.html
	git commit -m "updating gh-pages"
	git push --force --set-upstream origin gh-pages
	git checkout master

.PHONY: notebook serve push
