import {Card} from "antd"

function TodoCard() {

  return (
    <div>
        <Card
          title="do something number 1"
//           extra={<a href="#">More</a>}
          style={{
            margin: 50,
            width: 500,
          }}
        >
          <p>description</p>
          <p>additional info</p>
        </Card>
    </div>
  )
}

export default TodoCard
