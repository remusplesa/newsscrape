import React, {useState, useEffect} from 'react';
import axios from 'axios';
import '../styles/_container.scss'

const Analytics = () => {
    const [words, setWords] = useState([])

    useEffect(() => {
        axios.get("http://localhost:8000/top_keywords/")
        .then((response) => {
            setWords(response.data.results)
            console.log(response.data)
        })
        .catch(err => console.error(err))
    },[])

    return (
        <div className='barplot'>
            {words.map((el) => {
                return(
                    <Bar count={el.count} word={el.word}></Bar>
                ) 
            })}
        </div>
    )
}

const Bar = (props) => (
    <div 
    style={{
        height:20,
        width: props.count*20,
        backgroundColor: '#ADB6C4',
        padding:2,
        borderRadius:999,
        border:'solid',
        borderColor:'gold',
        borderWidth:2
    }}>
        {props.word}: {props.count}
    </div>
)

export default Analytics;