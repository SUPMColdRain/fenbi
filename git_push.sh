python main.py
# git config -e
# change HTTPS: `https://github.com/<name>/<repo>.git`
# to SSH: `git@github.com:<name>/<repo>.git`
echo "--- git push start! ---"
git add .
git commit -m "auto update star question"
git push origin master
echo "---- git push end! ----"