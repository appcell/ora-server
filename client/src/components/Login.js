import React, { Component } from 'react'
import { 
  Button, 
  Modal,
  Grid,
  Form,
  Message
} from 'semantic-ui-react'

import { store } from '../store'
import { login } from '../actions/login'

class LoginModal extends Component {
  constructor(props){
    super(props)

    this.state = {
      username: '',
      password: '',
      modalOpen: false,
      loading: false
    }

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleOpen = this.handleOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
  }

  handleInputChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handleSubmit(event) {
    this.setState({loading: true})
    store.dispatch(
      login(this.state.username, this.state.password, this.handleClose)
    )
  }

  handleOpen()  { this.setState({ modalOpen: true }) }

  handleClose() { this.setState({ modalOpen: false, loading: false }) }

  render(){
    return (
      <Modal 
        trigger={
          <Button 
            onClick={this.handleOpen}
            inverted={this.props.inverted}>Login
          </Button>
        }
      >
        <Modal.Header>Log-in to your account</Modal.Header>
        <Modal.Content>
          <Grid textAlign='center' style={{ height: '100%' }} verticalAlign='middle'>
          <Grid.Column style={{ maxWidth: 400 }}>
            <Form size='large' loading={this.state.loading}>
              <Form.Input 
                name='username'
                fluid 
                icon='user' 
                iconPosition='left' 
                placeholder='E-mail address' 
                onChange={this.handleInputChange}
              />
              <Form.Input
                name='password'
                fluid
                icon='lock'
                iconPosition='left'
                placeholder='Password'
                type='password'
                onChange={this.handleInputChange}
              />
              <Button 
                color='blue' 
                fluid 
                size='large' 
                onClick={this.handleSubmit}
                >
                Login
              </Button>
            </Form>
            <Message>
              Forgot password? <a href='/route/reset'>Click here</a>
            </Message>
          </Grid.Column>
        </Grid>
        </Modal.Content>
      </Modal>
    )
  }
}

export default LoginModal