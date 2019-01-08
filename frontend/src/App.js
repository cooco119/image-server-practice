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
import OpenSeadragon from 'openseadragon';

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
      enabledImageList: false,
      imageUrl: null,
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
    this.getImageListByName = this.getImageListByName.bind(this);
    this.setImagesChildOfTableRow = this.setImagesChildOfTableRow.bind(this);
    this.getImageUrl = this.getImageUrl.bind(this);
    this.popupViewer = this.popupViewer.bind(this);
    // this.openSeaDragonViewer = this.openSeaDragonViewer.bind(this);
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
      this.setState({enabledImageList: true})
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
  async popupViewer(bucketName, imageName){
    let url = await this.getImageUrl(bucketName, imageName);
    if (url !== null){
      let viewerWindow = window.open("", 'viewer', 'toolbar=0,status=0,width=1280px,height=960px');
      let res = await axios.get(url);
      res = res.data;
      let public_url = process.env.PUBLIC_URL;
      viewerWindow.document.write('<div id="openseadragon1" style="width: 1280px; height: 960px;"></div>\n<script src="'+public_url+'/openseadragon.min.js"></script>\n<script>var viewer = OpenSeadragon({ \
          element: "openseadragon1", \
          tileSources: { \
            type: "image", \
            url:"'+ res+'" \
          }, \
          showNavigator: true, \
        })</script>');
    } 
    else {
      alert("Error fetching image url");
    }
  }
  // openSeaDragonViewer(url){
  //   let viewer = OpenSeadragon({
  //     id: "openseadragon1",
  //     tileSources: {
  //       type: "image",
  //       url: res
  //     },
  //     showNavigator: true,
  //   })
  //   return;
  // }

  async getImageUrl(bucketName, imageName){
    let url = `/imageviewer/images/${bucketName}/${imageName}`;
    console.log("hello");
    return await axios.get(url)
    .then( async res => {
      let responseData = JSON.parse(res.data);
      if (res.status === 200){
        let url = responseData.url;
        // console.log(url);
        // this.setState({imageUrl: url});
        return url;
      }
      else{
        alert('fetching get image url failed')
        return;
      }
    })
  }

  getImageListByName(imageList){
    if (this.state.enabledImageList){
      let listRowElems = [];
      for (var i = 0; i < imageList.length; i++){
        let curImage = imageList[i];
        let t;
        let id = <td><label>{i.toString()}</label></td>;
        let bucketName = <td><label>{curImage.image_oid__bucket_name}</label></td>;
        let imageName = <td><label onClick={() => this.popupViewer(curImage.image_oid__bucket_name, curImage.image_name)}>{curImage.image_name}</label></td>;
        let user = <td><label>{curImage.user__name}</label></td>;
        let publicity = <td><label>Public</label></td>;
        if (curImage.is_private){
          publicity = <td><label>Private</label></td>;
        }
        let date = <td><label>{curImage.pub_date}</label></td>;
        let listRow = [id, bucketName, imageName, user, publicity, date]
        listRowElems.push(<tr>{listRow}</tr>);
      }
      // console.log(listRowElems);
      // console.log(<tr>test</tr>)
      return (
        <tbody>{listRowElems}</tbody>
      )
    }
  }

  setImagesChildOfTableRow(listRow, rowNum){
    let m_tr = document.createElement('tr');
    let att = document.createAttribute('id');
    att.value = rowNum.toString();
    m_tr.setAttributeNode(att);

    for (var i = 0; i <listRow.length; i++){
      m_tr.appendChild(listRow[i]);
    }
    return m_tr;
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

  async getImageServerInfo(bucketName, imageName){
    let url = `/imageuploader/upload/${bucketName}/${imageName}`;
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
      let f = files[i];
      if (!f.type.match('image.*')){
        alert('File should be images only.')
        return;
      }
      console.log(filestring);
      let filestream = fileReaderStrem(f);
      console.log(filestream);
      let bucketName = this.state.bucketName;
      let imageName = f.name;
      let imageServerInfo = await this.getImageServerInfo(bucketName, imageName);
      let url = imageServerInfo.url;
      let msg = imageServerInfo.msg;

      // const formData = new FormData();
      // formData.append(imageName, f);
      // axios.put(url,formData)
      //   .then((res) => {
      //     console.log(res)
      //     if (res.status !== 200){
      //       console.error('image put failed')
      //       return;
      //     }
      //     else{
      //       console.log('image #' + i.toString() + ' upload successful')
      //     }
      //   })

      reader.onloadend = (e) => {
        console.log(e);
        axios.put(url, e.target.result)
        .then((res) => {
          console.log(res)
          if (res.status !== 200){
            console.error('image put failed')
            return;
          }
          else{
            console.log('image #' + i.toString() + ' upload successful')
          }
        })
      }
      reader.readAsDataURL(f);
      
      // console.log("Checking if bucket exists")
      // minioClient.bucketExists(bucketName, function(err, exists) {
      //   // console.log(err)
      //   // console.log(exists)
      //   if (!exists){
      //     minioClient.makeBucket(bucketName, 'ap-southeast-1', function(err){
      //       if (err) {
      //         return alert(err)
      //       }
      //       else{
      //         console.log('Bucket created successfully in "ap-southeast-1".')
      //       }
      //     })
      //   }
      //   if (exists){
      //     return console.log('Bucket already exists')
      //   }
      //   if (err){
      //     console.log("Error occured checking bucket exists")
      //   }
      // })
      
      // minioClient.putObject(bucketName, imageName, filestream, (err, etag ) => {
      //   let etags = this.state.etags;
      //   let m_etag;
      //   m_etag = getEtag;
      //   etags.push(m_etag);
      //   this.setState({etags: etags})
      // })
      let appUrl = '/imageuploader/upload/';
      let d = new Date();
      d = new Date(d.getTime() - 3000000);
      let data = {
        "image_name": imageName,
        "image_format": imageName.split('.')[1],
        "image_data": {
          "bucketName": bucketName,
          "objectName": imageName
        },
        "user": this.state.loginvalue,
        "is_private": this.state.priavacy,
        "pub_date": d.getFullYear().toString()+"-"+((d.getMonth()+1).toString().length===2?(d.getMonth()+1).toString():"0"+(d.getMonth()+1).toString())+"-"+(d.getDate().toString().length===2?d.getDate().toString():"0"+d.getDate().toString())+" "+(d.getHours().toString().length===2?d.getHours().toString():"0"+d.getHours().toString())+":"+((parseInt(d.getMinutes()/5)*5).toString().length===2?(parseInt(d.getMinutes()/5)*5).toString():"0"+(parseInt(d.getMinutes()/5)*5).toString())+":00"
      }
      await axios.post(appUrl, JSON.stringify(data), {headers: {"content-type": "application/json"}})
      .then( res => {
        console.log(res.status)
        if (res.status === 201){
          console.log('image #' + i.toString() + ' uploaded successfully to db');
          return;
        }
        else if(res.status === 409){
          console.log('image #' + i.toString() + ' already exists in db');
          return;
        }
        else{
          console.log('image #' + i.toString() + ' upload failed with error messeage of : ' + `\n${JSON.parse(res.data).msg}`);
          return;
        }
      })
    }
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
          <div style={{flexDirection: 'row'}}>
            <table cellPadding="10" cellSpacing="10">
              <tr>
                <th>Id</th>
                <th>Bucket Name</th>
                <th>Image Name</th>
                <th>Uploader</th>
                <th>Publicity</th>
                <th>Date Time</th>
              </tr>
              {this.getImageListByName(this.state.imageList)}
            </table>
          </div>
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
