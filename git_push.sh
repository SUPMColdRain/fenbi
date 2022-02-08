echo "--- git push start! ---"
git add .
git commit -m "auto update"
git pull --rebase origin master
git push origin master
echo "---- git push end! ----"