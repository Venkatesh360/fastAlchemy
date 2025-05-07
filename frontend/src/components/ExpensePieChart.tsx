import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';


type Expense = {
    id: number;
    category: string;
    amount: number;
    description: string;
    created_at: string;
    updated_at: string;
  };

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#A28EFF'];

function ExpensePieChartWithTable({ expenses }: { expenses: Expense[] }) {
  // Group and total expenses by category
  const data = Object.values(
    expenses.reduce((acc, expense) => {
      if (!acc[expense.category]) {
        acc[expense.category] = {
          category: expense.category,
          amount: 0
        };
      }
      acc[expense.category].amount += expense.amount;
      return acc;
    }, {} as Record<string, { category: string; amount: number }>)
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h2>Expenses by Category</h2>

      <PieChart width={400} height={300}>
  <Pie
    data={data}
    dataKey="amount"
    nameKey="category" // this determines what's shown next to the dot
    cx="50%"
    cy="50%"
    outerRadius={100}
  >
    {data.map((entry, index) => (
      <Cell key={index} fill={COLORS[index % COLORS.length]} />
    ))}
  </Pie>
  <Tooltip />
  <Legend />
</PieChart>

      <table border={1} cellPadding={10} style={{ marginTop: '20px', width: '80%' }}>
        <thead>
          <tr>
            <th>Category</th>
            <th>Total Amount</th>
          </tr>
        </thead>
        <tbody>
          {data.map((entry, idx) => (
            <tr key={idx}>
              <td>{entry.category}</td>
              <td>${entry.amount.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ExpensePieChartWithTable;
