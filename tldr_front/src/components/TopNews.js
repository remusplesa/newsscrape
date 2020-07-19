import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/_container.scss";

const TopNews = () => {
  const url = "http://localhost:8000/top_articles/";

  const [top, setTop] = useState([]);

  useEffect(() => {
    axios.get(url).then((res) => {
      setTop(res.data.results);
      console.log("Top news: ", res.data);
    });
  }, []);

  return (
    <div className="newsBox">
      <h3>Top Stiri</h3>
      {top.map((element) => {
        return (
          <NewsBoxContainer
            title={element.title}
            source={element.source}
            key={element.id}
          ></NewsBoxContainer>
        );
      })}
    </div>
  );
};

const NewsBoxContainer = (props) => (
  <div>
    <a href={props.source} target="_blank">
      <h4>{props.title}</h4>
    </a>
  </div>
);

export default TopNews;
