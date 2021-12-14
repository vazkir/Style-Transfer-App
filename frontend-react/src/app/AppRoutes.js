import React from "react";
import { Route, Switch, Redirect } from 'react-router-dom';
import Home from "../components/Home";
import Error404 from '../components/Error/404';
import Currentmodel from '../components/Currentmodel';
import LatentManipulate from '../components/LatentManipulate';
import StyleTransfer from '../components/StyleTransfer';



const AppRouter = (props) => {

  console.log("================================== AppRouter ======================================");

  return (
    <React.Fragment>
      <Switch>
        <Route path="/" exact component={Home} />

        <Route path="/laten_manipulate" exact component={LatentManipulate} />
        {/* <Route path="/leaderboard" exact component={Leaderboard} /> */}
        <Route path="/style_transfer" exact component={StyleTransfer} />
        <Route path="/currentmodel" exact component={Currentmodel} />
        <Route component={Error404} />
      </Switch>
    </React.Fragment>
  );
}

export default AppRouter;