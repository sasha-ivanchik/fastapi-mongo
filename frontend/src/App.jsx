import React, { useState } from 'react'
import TodoCard from "./components/TodoCard.jsx"
import { Menu } from 'antd';


const navItems = [
  {
    label: 'Navigation One',
    key: 'one',
  },
  {
    label: 'Navigation Two',
    key: 'two',
  },
  {
    label: 'Navigation Three',
    key: 'three',
  },
];


function App() {
    const [current, setCurrent] = useState();
    const onClick = (e) => {
        console.log('click ', e);
        setCurrent(e.key);
    };
    return (
    <>
        <Menu
            onClick={onClick}
            selectedKeys={[current]}
            mode="horizontal"
            items={navItems}
        />
        <TodoCard/>
        <TodoCard/>
    </>
    )
}

export default App
