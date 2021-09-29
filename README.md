# openCyph

This project is used to complement CSC2004 - Cyber Security Fundamentals, Assessed Coursework 1
This project focuses on steganography, allowing users to encoded secret messages into specified payloads.

## API Reference

#### Get all items

```http
  GET /getImage
```

| Parameter | Type     | Description                                  |
| :-------- | :------- | :------------------------------------------- |
| `type`    | `string` | **Required**. `coverObject` or `stegoObject` |

#### Get item

```http
  POST /startStego
```

| Parameter | Type  | Description       |
| :-------- | :---- | :---------------- |
| `tbc`     | `tbc` | **Required**. tbc |

#### add(num1, num2)

Takes two numbers and returns the sum.

## Acknowledgements

- [YI XUAN]()

## Badges

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)

## Tech Stack

**Client:** React

**Server:** Python3

## Run Locally

Clone the project

```bash
  git clone https://github.com/yxchia98/openCyph/
```

Go to the project directory

```bash
  cd openCyph
```

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run start
```

Start API server

```bash
  python3 app.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
