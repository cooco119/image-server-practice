import React, { Component } from 'react';
import './App.css';
import axios from 'axios';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import ReactDOM from 'react-dom';
import GridElement from './MakeGridElement.jsx';
import * as Minio from 'minio';
import { string, func } from 'prop-types';
import * as fileReaderStrem from 'filereader-stream';

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
      nameListDict: null,
      nameListDictReady: false,
      uploading: false,
      selectedName: '',
      bucketName: '',
      priavacy: false,
      etags: [],
    }
    this.handleSigninChange = this.handleSigninChange.bind(this);
    this.handleSigninSubmit = this.handleSigninSubmit.bind(this);
    this.handleRegiesterChange = this.handleRegiesterChange.bind(this);
    this.handleRegiesterSubmit = this.handleRegiesterSubmit.bind(this);
    this.handleGridClick = this.handleGridClick.bind(this);
    this.loadUploader = this.loadUploader.bind(this);
    this.unloadUploader = this.unloadUploader.bind(this);
    this.logOut = this.logOut.bind(this);
    this.upload = this.upload.bind(this);
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
      this.setState({selectedName: name});
    })
  }

  Signin() {
    if (!this.state.isLoggedIn){
      return (
        <div>
          <form onSubmit={this.handleSigninSubmit}>
          <label>
            Name:
            <input type="text" value={this.state.loginvalue} onChange={this.handleSigninChange} />
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
            <input type="text" value={this.state.registervalue} onChange={this.handleRegiesterChange} />
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
          let m_nameListDict = [];
          let names = responseData.names;
          let user = this.state.loginvalue;
          for (var i = 0; i < names.length; i++){
            m_nameListDict.push({"user": user, "name": names[i], "handler": this.handleGridClick});
          }
          this.setState({nameListDict: m_nameListDict, nameListDictReady: true});
          // console.log(this.state.nameListDict);
        }
        else {
          alert(`Network error, try again.\nError message:${msg}`);
        }
      })
    }
    else{
      if (this.state.nameListDictReady){
        return (
          <Grid container id='grid-container' spacing={24}>
            {/* {console.log(this.state.names.map())} */}
            {this.createGrid(this.state.nameListDict)}
          </Grid>
        )
      } 
    }
  }
  createGridElement = function(nameKV) {
      return <GridElement name={nameKV.name} user={nameKV.user} handler={nameKV.handler}/>;
  }

  createGrid = function(nameListDict){
    // console.log(nameListDict);
    return nameListDict.map(this.createGridElement);
  }

  loadUploader() {
    if (!this.state.uploading){
      this.setState({uploading: true});
    }
  }

  unloadUploader() {
    if (this.state.uploading){
      this.setState({uploading: false, bucketName: '', imageName: '', priavacy: false});
    }
  }

  logOut() {
    if (this.state.isLoggedIn){
      this.setState({isLoggedIn: false, gotWorkspaces: false});
    }
  }

  async getImageServerInfo(){
    let url = `/imageuploader/upload?bucket=${this.state.bucketName}&object=${this.state.imageName}`;
    return await axios.get(url).then( res =>{
      let responseData = JSON.parse(res.data);
      if (res.status === 200){
        console.log('image server info');
        console.log(responseData);
        return responseData;
      }
      else{
        return;
      }
    })
  }

  async upload(){
    console.log(this.state.files)
    let files = this.state.files;
    this.setState({etag: []});
    if (files.length === 0){
      alert('Select files first!');
      return;
    }
    
    let imageServerInfo = await this.getImageServerInfo();

    let url = imageServerInfo.url;
    let acKey = imageServerInfo.keys.accessKey;
    let scKey = imageServerInfo.keys.secretKey;
    
    let minioClient = new Minio.Client({
      endPoint: '127.0.0.1',
      port: 9000,
      useSSL: false,
      accessKey: acKey,
      secretKey: scKey
    })
    for (var i= 0; i < files.length; i++){
      let reader = new FileReader();
      let filestring;
      reader.onerror = (e) => {
        console.error(e);
      }
      // reader.onprogress = updateProgress;
      reader.onabort = (e) => {
        alert('Upload cancled')
      }
      // reader.onload = (e) => {
      //   return filestring = e.target.result;
      // }
      let f = files[i];
      if (!f.type.match('image.*')){
        alert('File should be images only.')
        return;
      }
      reader.readAsBinaryString(f);
      console.log(filestring);
      let filestream = fileReaderStrem(f);
      console.log(filestream);
      let bucketName = this.state.bucketName;
      let imageName = f.name;
      minioClient.bucketExists(bucketName, function(err, exists) {
        if (err){
          minioClient.makeBucket(bucketName, 'ap-southeast-1', function(err){
            if (err) {
              return alert(err)
            }
            else{
              console.log('Bucket created successfully in "ap-southeast-1".')
            }
          })
        }
        if (exists){
          return console.log('Bucket already exists')
        }
      })
      
      minioClient.putObject(bucketName, imageName, filestream, function(err, etag){
        if (err !== null){
          let m_etags = this.state.etags;
          m_etags.push(etag);
          console.log('File #'+string(i)+' is uploaded successfully');
          this.setState({etags: m_etags});
          
          return;
        }
        console.error(err);
        alert(err);
        return;
      })
      let appUrl = '/imageuploader/upload';
      let data = {
        "image_name": imageName,
        "image_format": imageName.split('.')[1],
        "image_data": {
          "bucketName": bucketName,
          "objectName": this.state.etags
        },
        "user": this.state.loginvalue,
        "is_private": this.state.priavacy,
        "pub_date": new Date().toLocaleString()
      }
      await axios.post(appUrl, JSON.stringify(data), {headers: {"content-type": "application/json"}})
      .then( res => {
        if (res.status === 200){
          alert('image uploaded successfully');
          return;
        }
        else{
          alert('image upload failed with error messeage of : ' + `\n${JSON.parse(res.data).msg}`);
          return;
        }
      })
    }
  }

  getImageListByName(){
    
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
    if (this.state.uploading){
      return (
        <div style={{paddingLeft: 30, paddingTop: 50}}>
          <div style={{height:50}}>
            <header>
              <h1>Image Uploader Page</h1>
            </header>
          </div>
          <div style={{paddingTop: 30}}>
            <button style={{padding: 20, textAlign: 'center'}} onClick={this.unloadUploader}>Back</button>
          </div>
          <div>
            <h3 style={{padding: 20}}>Upload options</h3>
            <div id='bucket-name'>
              <div>
                <label>
                  Bucket Name:
                  <input type="text" value={this.state.bucketName} onChange={(event) => this.setState({bucketName: event.target.value})}/>
                </label>
              </div>
            </div>
            <div style={{height: 20}}></div>
            <div id='priavacy-selection'>
              <div>
                <label>
                  Public: 
                  <input type="radio" value="Public" onChange={(event) => this.setState({priavacy: false})} checked={!this.state.priavacy}/>
                </label>
                <label>
                  Private: 
                  <input type="radio" value="Private" onChange={(event) => this.setState({priavacy: true})} checked={this.state.priavacy}/>
                </label>
              </div>
            </div>
            <div style={{height: 20}}></div>
            <div id='file-path'>
            <form onSubmit={this.handleSigninSubmit}>
              <label>
                File:
                <input id='files' type="file" value={this.state.file} multiple onChange={e => this.setState({files: e.target.files})}/>
              </label>
              {/* <button onClick={document.getElementById('file').click()}>Open</button> */}
            </form>
            </div>
          </div>
          <hr></hr>
          <div>
            <button style={{padding: 10, textAlign: 'center'}} onClick={this.upload}>Upload</button>
          </div>
        </div>
      )
    }
    return (
      <div style={{paddingLeft: 30, paddingTop: 50}}>
        <div style={{height: 50}}>
          <header>
            <h1>Image Viewer Page</h1>
          </header>
        </div>
        <h3>Logged in as : {this.state.loginvalue}</h3>
        <button style={{padding:20, textAlign: 'center'}} onClick={this.logOut}>Logout</button>
        <hr></hr>
        <div style={{}}>
          <h3>Click to load uploader</h3>
          <button style={{padding: 20, textAlign: 'center'}} onClick={this.loadUploader}>Upload</button>
        </div>
        <hr></hr>
        <div>
          <h3>Select a workspace of a user</h3>
          {this.GetWorkspaces()}
          <hr></hr>
        </div>
        <div>
          <h3>Workspace of {this.state.selectedName}</h3>
        </div>
        <div style={{height: 200}}></div>
        <hr></hr>
        <div>
          <footer>
            <h6>Made By Markman</h6>
          </footer>
        </div>
      </div>
    );
  }
}

export default App;
