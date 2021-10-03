import React from 'react';
import { Link } from "react-router-dom";

export function Links(props) {
  return props.games.map((game) => (
    <Link to={`/games/${game.steam_id}`}>
      <img
        alt={`${game.game_name_on_steam} link`}
        src={game.app_detail.header_image_url} />
    </Link>
  ));
}
