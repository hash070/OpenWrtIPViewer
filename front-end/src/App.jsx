import React from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { Button, Input, message, Typography } from 'antd';
import { CopyOutlined } from '@ant-design/icons'
import './App.css'
import axios from 'axios';

const { Title } = Typography;

class App extends React.Component {
  state = {
    lastdate: '',
    value: '',
    copied: false,
  };

  componentDidMount() {
    axios.post('/getIP')
      .then(response => {
        this.setState({ value: response.data })
        console.log(response.data)
      })

    axios.post('/getLastDate')
      .then(response => {
        this.setState({ lastdate: response.data })
        console.log(response.data)
      })
  }

  render() {
    return (
      <div>
        <div className='InputBox'>
          <Title level={5}>Your OpenWrt WAN ip addr</Title>
          <Title level={5}>{this.state.lastdate}</Title>
          <Title level={5}>Click to copy it</Title>
          <CopyToClipboard text={this.state.value}
            onCopy={() => this.setState({ copied: true })}>
            <div>
              <input value={this.state.value} id='outputText'
                onChange={({ target: { value } }) => this.setState({ value, copied: false })} /><Button><CopyOutlined /></Button>
            </div>
          </CopyToClipboard>
          {this.state.copied ? <span style={{ color: 'green' }}>Copied.</span> : null}
        </div>
      </div>
    );
  }
}

export default App;