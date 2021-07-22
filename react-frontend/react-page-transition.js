import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Switch, Route, Link } from "react-router-dom";
// import { PageTransition } from "@steveeeie/react-page-transition";
import "./styles.css";

function Links(games) {
  return (<>
    <Link to="/games/Cities XXL">
      <img
        alt="Cities XXL link"
        src="https://cdn.akamai.steamstatic.com/steam/apps/313010/header.jpg?t=1602859660"
      />
    </Link>
    <Link to="/games/Cities XXL">
      <img
        alt="Cities XXL link"
        src="https://cdn.akamai.steamstatic.com/steam/apps/313010/header.jpg?t=1602859660"
      />
    </Link>
  </>)
};

const Home = () => (
  <div>
    <h1>Homee</h1>
    <Links />
  </div>
);

// All route props (match, location and history) are available to About
function About(props) {
  return (
    <div>
      <Link to="/"> Back </Link>
      <h1>Game name: {props.match.params.game_name}!</h1>
    </div>
  );
}

function App() {
  return (
    <React.StrictMode>
      <BrowserRouter>
        {/* Tabs go here and wrap the Route component - this is where I took Links from  */}
        <Route
          render={({ location }) => {
            return (
              // <PageTransition
              // transitionKey={location.pathname}
              // enterAnimation="moveFromTopFade"
              // exitAnimation="moveToBottomFade"
              // >
                <Switch location={location}>
                  <Route exact path="/" component={Home} />
                  <Route path="/games/:game_name" component={About} />
                </Switch>
              // </PageTransition>
            );
          }}
        />
      </BrowserRouter>
    </React.StrictMode>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
