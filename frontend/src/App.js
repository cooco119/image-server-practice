import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import ReactDOM from 'react-dom';
import GridElement from './MakeGridElement.jsx';

class App extends Component {
  constructor(props){
    super(props)
    this.state = {
      loginvalue: '',
      registervalue: '',
      isLoggedIn: false,
      notice: '',
      gotNotice: false,
      isRegistered: false,
      msg1: '',
      msg2: '',
      responded: false,
      gotWorkspaces: false,
      names: null,
      imageList: null,
    }
    this.handleSigninChange = this.handleSigninChange.bind(this);
    this.handleSigninSubmit = this.handleSigninSubmit.bind(this);
    this.handleRegiesterChange = this.handleRegiesterChange.bind(this);
    this.handleRegiesterSubmit = this.handleRegiesterSubmit.bind(this);
    this.handleGridClick = this.handleGridClick.bind(this);
  }

  componentWillMount(){
    this.GetNotice();
  }
  
  handleSigninChange(event) {
    this.setState({loginvalue: event.target.value});
  }

  handleSigninSubmit(event) {
    event.preventDefault();
    let url = '/home/signin/';
    let headers = {
      'Content-Type': 'application/json',
    }
    let data = {
      "name": this.state.loginvalue
    }
    axios.post(url, data, {headers: headers})
    .then(res => {
      let resData = JSON.parse(res.data);
      this.setState({msg1: resData.msg});
      if (res.status === 200){
        this.setState({isLoggedIn: true});
        alert('Sign in successful!');
      }
      else{
        alert('No matching user. Register please.')
      }
    })

  }

  handleRegiesterChange(event) {
    this.setState({registervalue: event.target.value});
  }

  handleRegiesterSubmit(event) {
    event.preventDefault();
    let url = '/home/register/';
    let headers = {
      'Content-Type': 'application/json',
    }
    let data = {
      "name": this.state.registervalue
    }
    axios.post(url, data, {headers: headers})
    .then(res => {
      let resData = JSON.parse(res.data);
      this.setState({msg2: resData.msg});
      if (res.status === 200){
        this.setState({isRegistered: true});
        alert('Register successful!');
      }
      else{
        alert('User Exists')
      }
    })

  }

  handleGridClick(name) {
    let url = `/imageviewer/${this.state.loginvalue}/workspaces/${name}`;
    axios.get(url)
    .then( res => {
      let responseData = JSON.parse(res.data);
      if (res.status === 200){
        this.setState({imageList: responseData.img_list});
      }
      console.log(this.state.imageList);
    })
  }

  Signin() {
    if (!this.state.isLoggedIn){
      return (
        <div>
          <form onSubmit={this.handleSigninSubmit}>
          <label>
            Name:
            <input type="text" value={this.state.value} onChange={this.handleSigninChange} />
          </label>
          <input type="submit" value="Submit" />
        </form>
        <label>{this.state.msg1}</label>
        </div>
      )
    }
    else {
      return (
        <div>
          <h5>Logged in successfully!</h5>
        </div>
      )
    }
  }

  GetNotice() {
    if (this.state.gotNotice === false){
      axios.get('/home/notice/')
      .then( async res =>{
        if (res.status === 200 ){
          let responseData = JSON.parse(res.data);
          this.setState({notice: responseData.notice})
        }
      })
      this.setState({gotNotice: true});
    }
  }

  Notice() {
    if (this.state.gotNotice === false){
      return(
        <div>
          <label>Fetching notice..</label>
        </div>
      )
    }
    else{
      return (
        <div>
          <label>{this.state.notice}</label>
        </div>
      )

    }
  }

  Register() {
    // if (!this.state.isRegistered){
      return (
        <div>
          <form onSubmit={this.handleRegiesterSubmit}>
          <label>
            Name:
            <input type="text" value={this.state.value} onChange={this.handleRegiesterChange} />
          </label>
          <input type="submit" value="Submit" />
        </form>
        <label>{this.state.msg2}</label>
        </div>
      )
    // }
    // else {
    //   return (
    //     <div>
    //       <h5>Registered successfully!</h5>
    //     </div>
    //   )
    // }
  }

  GetWorkspaces(){
    if (!this.state.gotWorkspaces){
      let url = `/imageviewer/${this.state.loginvalue}/workspaces`;
      axios.get(url)
      .then( res => {
        let responseData = JSON.parse(res.data);
        let msg = responseData.msg;
        if (res.status === 200){
          this.setState({names: responseData.names, gotWorkspaces: true});
        }
        else {
          alert(`Network error, try again.\nError message:${msg}`);
        }
      })
    }
    else{
      return (
        <Grid container id='grid-container' spacing={24}>
          {/* {console.log(this.state.names.map())} */}
          {this.createGrid(this.state.names)}
        </Grid>
      )
    }
  }
  createGridElement = function(elemName) {
      return <GridElement name={elemName} handler={(user) => {
        let url = `/imageviewer/${user}/workspaces/${elemName}`;
        axios.get(url)
        .then( res => {
          let responseData = JSON.parse(res.data);
          if (res.status === 200){
            this.setState({imageList: responseData.img_list});
          }
          console.log(this.state.imageList);
        })
      }}/>;
  }

  createGrid = function(nameList){
    return nameList.map(this.createGridElement)
  }

  // makeGrid(namesList){
  //   let len = namesList.length;
  //   let container = document.getElementById('grid-container');
  //   console.log(container)
  //   const elements = []
  //   for (var i = 0; i < len; i++){
  //     let instance = this.makeGridElement(namesList[i])
  //     // console.log(typeof(instance));
  //     elements.push(instance);
  //     container.innerHTML = elements;
  //   }
  //   console.log(elements[0]);
  //   container.appendChild(elements);
  // } 

  // const Grid1 = (props)=>{
  //   const { name } = props;
  //   return (
  //     <Grid item>
  //     <Paper>{name}</Paper>
  //   </Grid>
  //   );
  // }

  makeGridElement(name) {
    return (
      <div>
      <Grid item>
        <Paper>{name}</Paper>
      </Grid>
      </div>
    )
  }

  render() {
    if (this.state.isLoggedIn === false){
      return (
        <div style={{paddingLeft: 30, paddingTop: 50}}>
          <div style={{height: 50}}>
            <header>
              <h1>Image Server Practice</h1>
            </header>
          </div>
          <h3>Notice : </h3>
          {this.Notice()}
          <div style={{height: 10}}></div>
          <hr></hr>
          <div style={{height: 30}}></div>
          <h3>Login : </h3>
          {this.Signin()}
          <div style={{height: 30}}></div>
          <h3>Register : </h3>
          {this.Register()}
          <div>
          </div>
        </div>
      );
    }
    return (
      <div style={{paddingLeft: 30, paddingTop: 50}}>
          <div style={{height: 50}}>
            <header>
              <h1>Image Viewer Page</h1>
            </header>
          </div>
          <h3>Logged in as : {this.state.loginvalue}</h3>
          <hr></hr>
          <div>
            <div>
              {this.GetWorkspaces()}
            </div>
          </div>
        </div>
    );
  }
}

export default App;
