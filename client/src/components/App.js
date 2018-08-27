import PropTypes from 'prop-types'
import React, { Component } from 'react'
import { connect } from 'react-redux'
import { withRouter } from 'react-router-dom'
import { store } from '../store'
import {
  Button,
  Container,
  Grid,
  Header,
  Icon,
  Image,
  List,
  Menu,
  Responsive,
  Segment,
  Sidebar,
  Visibility,
  Dropdown
} from 'semantic-ui-react'

import { Route, Switch } from 'react-router' 

import LoginModal from './Login'

import { logout } from '../actions/login'

const LoginMenuItems = (props) => (
  <Menu.Item position='right'>
    <LoginModal 
      inverted={props.inverted} 
      errorMessage={props.errorMessage}
    />
    <Button as='a' inverted={props.inverted} primary={!props.inverted} style={{ marginLeft: '0.5em' }}>
      Sign Up
    </Button>
  </Menu.Item>
)

const UserMenuItems = (props) => (
  <Menu.Item position='right'>
    <Dropdown icon='user' text={props.email} pointing className='link item'>
      <Dropdown.Menu>
        <Dropdown.Header>User Options</Dropdown.Header>
        <Dropdown.Item>My Account</Dropdown.Item> 
        <Dropdown.Divider />
        <Dropdown.Item onClick={()=>{store.dispatch(logout())}}>Log out</Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  </Menu.Item>
)

class DesktopContainer extends Component {
  state = {}

  hideFixedMenu = () => this.setState({ fixed: false })
  showFixedMenu = () => this.setState({ fixed: true })

  render() {
    const { children } = this.props
    const { fixed } = this.state

    let rightMenu = this.props.loginInfo && this.props.loginInfo.email ? 
      <UserMenuItems 
        email={this.props.loginInfo.email}
      /> :
      <LoginMenuItems 
        inverted={!fixed}
        errorMessage={this.props.errorMessage}
      />

    return (
      <Responsive minWidth={Responsive.onlyTablet.minWidth}>
        <Visibility
          once={false}
          onBottomPassed={this.showFixedMenu}
          onBottomPassedReverse={this.hideFixedMenu}
        >
          <Segment
            inverted
            textAlign='center'
            style={{ minHeight: 80, padding: '1em 0em' }}
            vertical 
          >
            <Menu
              fixed={fixed ? 'top' : null}
              inverted={!fixed}
              pointing={!fixed}
              secondary={!fixed}
              size='large' 
            >
              <Container>
                <Menu.Item as='a' active>
                  Home
                </Menu.Item>
                <Menu.Item as='a'>Work</Menu.Item>
                {rightMenu}
              </Container>
            </Menu>
          </Segment>
        </Visibility>
        {children}
      </Responsive>
    )
  }
}

DesktopContainer.propTypes = {
  children: PropTypes.node,
}

class MobileContainer extends Component {
  state = {}

  handlePusherClick = () => {
    const { sidebarOpened } = this.state

    if (sidebarOpened) this.setState({ sidebarOpened: false })
  }

  handleToggle = () => this.setState({ sidebarOpened: !this.state.sidebarOpened })

  render() {
    const { children } = this.props
    const { sidebarOpened } = this.state

    let rightMenu = this.props.loginInfo && this.props.loginInfo.email ? 
      <UserMenuItems 
        email={this.props.loginInfo.email}
      /> :
      <LoginMenuItems 
        inverted={!this.props.fixed} 
        errorMessage={this.props.errorMessage}
      />

    return (
      <Responsive maxWidth={Responsive.onlyMobile.maxWidth}>
        <Sidebar.Pushable>
          <Sidebar as={Menu} animation='uncover' inverted vertical visible={sidebarOpened}>
            <Menu.Item as='a' active>
              Home
            </Menu.Item>
            <Menu.Item as='a'>Work</Menu.Item>
          </Sidebar>

          <Sidebar.Pusher
            dimmed={sidebarOpened}
            onClick={this.handlePusherClick}
            style={{ minHeight: '100vh' }}
          >
            <Segment
              inverted
              textAlign='center'
              style={{ minHeight: 80, padding: '1em 0em' }}
              vertical
            >
              <Container>
                <Menu inverted pointing secondary size='large'>
                  <Menu.Item onClick={this.handleToggle}>
                    <Icon name='sidebar' />
                  </Menu.Item>
                  {rightMenu}
                </Menu>
              </Container>
            </Segment>

            {children}
          </Sidebar.Pusher>
        </Sidebar.Pushable>
      </Responsive>
    )
  }
}

MobileContainer.propTypes = {
  children: PropTypes.node,
}

const WelcomePage = () => (
  <div>
    <Segment 
      inverted 
      textAlign='center'
      style={{
        minHeight: 300
      }}
    >
      <Header
        as='h1'
        content='ORA Data Platform'
        inverted
        style={{
          paddingTop: '1.5em',
          fontSize: '3em',
          fontWeight: 'normal',
        }}
      />
      <Header
        as='h2'
        content='A dive into competitive Overwatch data.'
        inverted
        style={{
          fontSize: '1.7em',
          fontWeight: 'normal',
          marginTop: '0.5em',
        }}
      />
    </Segment>
    <Segment style={{ padding: '8em 0em' }} vertical>
      <Grid container stackable verticalAlign='middle'>
        <Grid.Row>
          <Grid.Column width={8}>
            <Header as='h3' style={{ fontSize: '2em' }}>
              Check Out Our Analyzer Client
            </Header>
            <p style={{ fontSize: '1.33em' }}>
              Overwatch Replay Analyzer (ORA) is a free software developed by OWDATA.ORG, 
              a free organization devoted to competitive Overwatch data analysis.
            </p>
          </Grid.Column>
          <Grid.Column floated='right' width={6}>
            <Image bordered rounded size='large' src='/static/media/ora-client.png' />
          </Grid.Column>
        </Grid.Row>
        <Grid.Row>
          <Grid.Column textAlign='center'>
            <Button 
              as='a'
              href='https://github.com/appcell/OverwatchDataAnalysis' 
              size='huge'
              target='_blank'
              rel='noopener noreferrer'
              >
              Check It Out
            </Button>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </Segment>
  </div>
)

const Footer = () => (
  <Segment inverted vertical style={{ padding: '5em 0em' }}>
    <Container>
      <Grid divided inverted stackable>
        <Grid.Row>
          <Grid.Column width={3}>
            <Header inverted as='h4' content='About' />
            <List link inverted>
              <List.Item as='a'>Sitemap</List.Item>
              <List.Item as='a'>Contact Us</List.Item>
              <List.Item as='a'>Partnership</List.Item>
            </List>
          </Grid.Column>
          <Grid.Column width={7}>
            <Header as='h4' inverted>
              Open Source Project
            </Header>
            <p>
              Contact us if you are able to help.
            </p>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </Container>
  </Segment>
)

const ResponsiveContainer = ({ children, loginInfo }) => (
  <div>
    <DesktopContainer loginInfo={loginInfo}>{children}</DesktopContainer>
    <MobileContainer loginInfo={loginInfo}>{children}</MobileContainer>
  </div>
)

ResponsiveContainer.propTypes = {
  children: PropTypes.node,
}

class App extends Component {
  render() {
    console.log(this.props)
    return(
      <ResponsiveContainer loginInfo={this.props.loginInfo}>
        <Switch>
          <Route exact path="/" render={() => (<WelcomePage />)} />
          <Route exact path="/route/home" render={() => (<div>Logged In!</div>)} />
        </Switch>
        <Footer />
      </ResponsiveContainer>
    )
  }
}

export default withRouter(connect(
  state => ({
    loginInfo: state.login
  })
)(App))