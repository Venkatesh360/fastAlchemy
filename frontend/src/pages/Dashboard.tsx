import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/UserContext";

type Expense = {
  id: number;
  category: string;
  amount: number;
  description: string;
  time: string;
  date: string;
};

function Dashboard() {
  const [update, setUpdate] = useState<Expense | null>(null);
  const [category, setCategory] = useState<string>("");
  const [amount, setAmount] = useState<number>(0);
  const [description, setDescription] = useState<string>("");
  const { token } = useAuth()

  const sampleExpenses = []

  useEffect(() => {
    const getExpenses = async () => {
      const res = axios.get("http://127.0.0.1:8000/api/expense/get_expense", {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(res => console.log(res.data))
        .catch(err => console.error(err));
        console.log(res)
    };

    getExpenses()
  }, [])

  const handleEdit = (expense: Expense) => {
    setUpdate(expense);
    setCategory(expense.category);
    setAmount(expense.amount);
    setDescription(expense.description);
  };

  const handleUpdate = () => {
    console.log({
      id: update?.id,
      category,
      amount,
      description,
    });
    // You could now update the backend or state here
    setUpdate(null);
  };

  const handleCreate = async () =>{
    const expense_obj = {
      category: category,
      amount: amount,
      description: description
    }

    const exp = await axios.post("http://127.0.0.1:8000/api/expense/create_expense", expense_obj,{
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    setCategory("")
    setCategory(0)
    setCategory("")
    console.log(exp)
  }

  const handleDelete = (id: number) => {
    console.log("Delete ID:", id);
    // You could remove the row from state or make an API call
  };

  return (
    <div>
      <h1>My Expenses</h1>
      <table border={2} cellPadding="10">
        <thead>
          <tr>
            <th>Category</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Time</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {sampleExpenses.map((expense) => (
            <tr key={expense.id}>
              <td>{expense.category}</td>
              <td>${expense.amount.toFixed(2)}</td>
              <td>{expense.description}</td>
              <td>{expense.time}</td>
              <td>{expense.date}</td>
              <td>
                <button onClick={() => handleEdit(expense)}>Update</button>
                <button
                  onClick={() => handleDelete(expense.id)}
                  style={{ marginLeft: "10px" }}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}

          {update && (
            <tr>
              <td>
                <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} />
              </td>
              <td>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(parseFloat(e.target.value))}
                />
              </td>
              <td>
                <input
                  type="text"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </td>
              <td></td>
              <td></td>
              <td>
                <button onClick={() => setUpdate(null)}>Cancel</button>
                <button onClick={handleUpdate} style={{ marginLeft: "10px" }}>
                  Update
                </button>
              </td>
            </tr>
          )}
          <tr>
            <th><input type="text" value={category} onChange={(e) => setCategory(e.target.value)} /></th>
            <th><input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} /></th>
            <th><input type="text" value={description} onChange={(e) => setDescription(e.target.value)} /></th>
            <th></th>
            <th></th>
            <th> <button onClick={handleCreate}>Create</button></th>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
