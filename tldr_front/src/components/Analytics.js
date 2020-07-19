import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/_container.scss";

const Analytics = () => {
  const [words, setWords] = useState([]);
  const [max, setMax] = useState(0);
  useEffect(() => {
    axios
      .get("http://localhost:8000/top_keywords/")
      .then((response) => {
        setWords(response.data.results);
        setMax(response.data.results[0].count);
        console.log("top words:", response.data);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="plot-area">
      {" "}
      <h3>Statistici</h3>
      <div className="barplot">
        {words.map((el) => {
          return <Bar count={el.count} word={el.word} max={max}></Bar>;
        })}
      </div>
    </div>
  );
};

const Bar = (props) => {
  let maxWidth = props.max;
  let width = (props.count * 90) / maxWidth;

  return (
    <div key={props.word} className="bar" style={{ width: `${width}%` }}>
      <span>
        {props.word}: {props.count}
      </span>
    </div>
  );
};

export default Analytics;
