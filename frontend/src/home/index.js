import React, { Component } from 'react';
import axios from 'axios';

class Home extends Component{
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
    }
    this.handleSigninChange = this.handleSigninChange.bind(this);
    this.handleSigninSubmit = this.handleSigninSubmit.bind(this);
    this.handleRegiesterChange = this.handleRegiesterChange.bind(this);
    this.handleRegiesterSubmit = this.handleRegiesterSubmit.bind(this);
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

  render(){
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

}

export default Home;
