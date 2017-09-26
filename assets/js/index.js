/* @flow */
var React = require('react')
var ReactDOM = require('react-dom')
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  Container,
  Row,
  Col,
  Jumbotron,
  Button
} from 'reactstrap';
import 'bootstrap/dist/css/bootstrap.css';


type Props = {
title: string,

 };

 type State = {
  checked: boolean;
  msg: string;
};

class Comment extends React.Component<Props, State>{
  constructor(props) {
    super(props);
    this.state = {
      checked: true,
      msg: "checked",
    };
  }
  //default state of variable



  edit(){
      alert('edit *itch')

  }
  remove(){
    alert('who cares')
  }


  handleChecked(){
//if the argument is checked than update text to that
    console.log(this.state.checked);
    if (this.state.checked){
      this.setState({checked: false, msg: "unchecked"})
    }
    else{
      this.setState({checked: true, msg: "checked"})
    }
  }

  render() {


    return <div className="commentContainer">
          <div className="commentText">{this.props.title}</div>
          <button onClick={this.edit} className="btn btn-success btn-xs">Edit</button>
          <button onClick={this.remove} className="btn btn-danger btn-xs">Remove</button>
          <input type="checkbox" onClick={this.handleChecked.bind(this)} defaultChecked={this.state.checked}/>
          <h3>Checkbox is {this.state.msg}</h3>

    </div>;
}
}

ReactDOM.render(<div><Comment title={"shit"}/>  </div>, document.getElementById('container'));
