import React from 'react';
import ReactDOM from 'react-dom';
import Search from './search';


const myModule = <Search />;
// let testModule = <div> test </div>

ReactDOM.render(
  myModule,
  document.getElementById('reactEntry'),
);

/*
ReactDOM.render(
    testModule,
    document.getElementById('reactEntry'),
  );
  */
