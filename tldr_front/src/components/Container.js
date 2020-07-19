import React from "react";
import "../styles/_container.scss";
import News from "../components/News";
import Analytics from "../components/Analytics";
import TopNews from "../components/TopNews";

const Container = () => {
  const date = new Date();

  return (
    <div className="container">
      <div className="main-container">
        <header>
          <h2>TLDR news app;</h2>
          <h2>
            {date.getDate()}.{date.getMonth()+1}.{date.getFullYear()}
          </h2>
        </header>
        <div className="analytics">
          <Analytics></Analytics>
          <TopNews></TopNews>
        </div>
        <News></News>
      </div>
    </div>
  );
};
export default Container;
