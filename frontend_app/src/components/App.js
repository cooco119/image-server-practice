import React from "react";
import ReactDOM from "react-dom";
import DataProvider from './DataProvider';
import Notice from "./Notice";

const App = () => (
  <DataProvider endpoint="home/notice/" 
                render={data => <Notice data={data} />} />
);
const wrapper = document.getElementById("app");

wrapper ? ReactDOM.render(<App />, wrapper) : <h2>Helloworld</h2>;