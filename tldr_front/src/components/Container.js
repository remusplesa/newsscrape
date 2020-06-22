import React from 'react';
import '../styles/_container.scss';
import News from '../components/News';
import Analytics from '../components/Analytics';

const Container = () => {
    return (
        <div className="container">
            <div className="main-container">
                <header>
                    <h2>Hello there</h2>
                </header>
                <div className="analytics">
                    <Analytics></Analytics>
                </div>
                <News></News> 
            </div>
        </div>
    )
}
export default Container;