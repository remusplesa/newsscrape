import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "../styles/_article.scss";

const News = () => {
  const limit = 12;
  const firstPage = 1;
  const url = "http://localhost:8000";

  const [news, setNews] = useState([]);
  const [page, setPage] = useState(
    `/articles/?pageNumber=${firstPage}&limit=${limit}`
  );
  const [load, setLoad] = useState(false);
  const observer = React.useRef(
    new IntersectionObserver(
      (entries) => {
        const first = entries[0];
        if (first.isIntersecting) {
          setLoad(true);
          console.log("loading...");
        }
      },
      { threshold: 1 }
    )
  );
  const [element, setElement] = useState(null);

  useEffect(() => {
    const currentElement = element;
    const currentObserver = observer.current;
    if (currentElement) {
      currentObserver.observe(currentElement);
    }

    axios
      .get(url + page)
      .then((res) => {
        setNews([...news, ...res.data.articles]);
        if (res.data.next_page) {
          setPage(res.data.next_page);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      if (currentElement) {
        currentObserver.unobserve(currentElement);
        setLoad(false);
      }
    };
  }, [element, load]);

  useEffect(() => {
    console.log("news: ", news, "page: ", page);
  }, [news, page]);

  return (
    <div className="news">
      {news.map((article) => {
        return (
          <Article
            key={article._id}
            url={url}
            article={article}
            image={article.img_source}
            title={article.title}
            source={article.source}
            text={article.tldr}
          ></Article>
        );
      })}
      <div
        style={{ marginTop: -50, width: 5, height: 5 }}
        ref={setElement}
      ></div>
    </div>
  );
};

const Article = (props) => {
  function increment() {
    axios
      .put(`${props.url}/articles/${props.article._id}?to_update=clicks`)
      .then((res) => console.log(res));
  }

  return (
    <div className="article">
      <img src={props.article.img_source}></img>

      <div>
        <h3>{props.article.title}</h3>
        <p>{props.article.tldr}</p>
        <button onClick={increment}>
          <a href={props.article.source} target="_blank">
            Articol intreg
          </a>
        </button>
      </div>
    </div>
  );
};
export default News;
