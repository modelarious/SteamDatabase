
# docker run -v C:\Users\micha\youtube wernight/youtube-dl --update
# docker commit -a modelarious -m "update wernight's youtube-dl image to modern youtube-dl" goofy_shtern modelarious/youtube-dl-updated
# docker run --rm -v C:\Users\micha\youtube\video_game_music modelarious/youtube-dl-updated -i -x https://www.youtube.com/playlist?list=PL_dTwmmhdnaQekY02D40GNlo-boSOI4-p
docker run --rm -v C:\Users\micha\youtube\video_game_music modelarious/youtube-dl-updated -k https://www.youtube.com/playlist?list=PL_dTwmmhdnaQekY02D40GNlo-boSOI4-p

FROM ubuntu