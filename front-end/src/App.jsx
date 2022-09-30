import React from 'react';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { Button, Input, message } from 'antd';
import { CopyOutlined } from '@ant-design/icons'
import './App.css'
import axios from 'axios';

class App extends React.Component {
  state = {
    value: '',
    copied: false,
  };

  componentDidMount() {
    axios.post('api/getIP')
      .then(response => {
        this.setState({ value: response.data })
        console.log(response.data)
      })
  }

  render() {
    return (
      <div>
        <div className='InputBox'>
          <CopyToClipboard text={this.state.value}
            onCopy={() => this.setState({ copied: true })}>
            <div>
              <input value={this.state.value}
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