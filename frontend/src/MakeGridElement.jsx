import React from 'react';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';

let GridElement = function statelessFunctionComponenetClass(props){
  return (
      <Grid item xs={3}>
        <button key={props.key} style={{padding: 10, textAlign: 'center'}} onClick={(event)=>props.handler(props.name)}>{props.name}</button>
      </Grid>
  )
}

export default GridElement;