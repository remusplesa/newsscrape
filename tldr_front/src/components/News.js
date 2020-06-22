import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../styles/_article.scss';

const News = () => {
    const [news, setNews] = useState({
        articles:[]
    });
    const [page, setPage] = useState(0)

    useEffect(() => {
        axios
            .get("http://localhost:8000/articles/", {
                params: {
                pageNumber: page,
                limit: 36,
                },
            })
            .then((res) =>{
                setNews(res.data)
                console.log(res.data)
            })
            .catch((error) => console.log(error));
    },[])

    return (
        <div className="news">
            {news.articles.map((article) => {
                return(
                    <Article
                        key={article._id}
                        image={article.img_source}
                        title={article.title}
                        source={article.source}
                        text={article.tldr}>
                    </Article>
                )
            })}
            <div style={{backgroundColor: "blue", height:3, width:"100%", margin:-4}}></div>
        </div>
    )
}

const Article = (props) => (
    <div className='article'>
        <img src={props.image} ></img>
        <div>
            <h3>{props.title}</h3>
            <p>{props.text}</p>
            <button>
                <a href={props.source} target="_blank">Articol intreg</a>
            </button>
        </div>
        
    </div>
)
export default News;