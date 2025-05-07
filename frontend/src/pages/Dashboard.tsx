import { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../context/UserContext";
import ExpensePieChart from "../components/ExpensePieChart";
import CreateExpense from "../components/CreateExpense";
import "./Dashboard.css"


type Expense = {
  id: number;
  category: string;
  amount: number;
  description: string;
  created_at: string;
  updated_at: string;
};

function Dashboard() {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [id, setId] = useState<number | null>(null)
  const [update, setUpdate] = useState<Expense | null>(null);
  const [category, setCategory] = useState<string>("");
  const [amount, setAmount] = useState<number>(0);
  const [description, setDescription] = useState<string>("");
  const { token } = useAuth()

  useEffect(() => {
    getExpenses()
  }, [])


  const getExpenses = async () => {
    const res = await axios.get("http://127.0.0.1:8000/api/expense/get_expense", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    setExpenses(res.data.expenses);

    console.log(res)
  };

  const handleEdit = (expense: Expense) => {
    setId(expense.id)
    setUpdate(expense);
    setCategory(expense.category);
    setAmount(expense.amount);
    setDescription(expense.description);
  };

  const handleUpdate = async () => {
    const update_obj = {
      expense_id: id,
      category: category,
      amount: amount,
      description: description
    }
    console.log(update_obj)

    const response = await axios.put("http://127.0.0.1:8000/api/expense/update_expense", update_obj, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    console.log(response)

    getExpenses()
    setUpdate(null);
  };



  const handleDelete = async (id: number) => {
    const res = await axios.delete(`http://127.0.0.1:8000/api/expense/delete_expense/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    console.log(res)
    getExpenses()
  };

  return (
    <div>
      <h1>My Expenses</h1>
      <ExpensePieChart expenses={expenses}/>
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
          {expenses.map((expense) => (
            <tr key={expense.id}>
              <td data-label="Category">{expense.category}</td>
              <td data-label="Amount">₹{expense.amount.toFixed(2)}</td>
              <td data-label="Description">{expense.description}</td>
              <td data-label="Time">{new Date(expense.updated_at).toLocaleTimeString("en-IN", {
                timeZone: "Asia/Kolkata",
                hour12: true
              })}</td>
              <td data-label="Date">{new Date(expense.updated_at).toLocaleDateString("en-IN", {
                timeZone: "Asia/Kolkata"
              })}</td>
              <td data-label="Actions">
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
        </tbody>
      </table>
      <h1>Create new expense</h1>
      <CreateExpense expenses={expenses} getExpenses={getExpenses} />
    </div>
  );
}

export default Dashboard;
