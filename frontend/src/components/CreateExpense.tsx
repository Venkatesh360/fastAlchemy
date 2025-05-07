import { useState } from 'react';
import { useAuth } from '../context/UserContext';
import axios from 'axios';
import "./CreateExpense.css"

type Expense = {
    id: number;
    category: string;
    amount: number;
    description: string;
    created_at: string;
    updated_at: string;
};

type CreateExpenseProps = {
    expenses: Expense[];
    getExpenses: () => void;
};

function CreateExpense({ expenses, getExpenses }: CreateExpenseProps) {
    const [selected, setSelected] = useState('');
    const [customValue, setCustomValue] = useState('');
    const [amount, setAmount] = useState<number | ''>(0);
    const [description, setDescription] = useState('');
    const isCustom = selected === 'Custom';

    const categories = Array.from(new Set(expenses.map(exp => exp.category)));
    const { token } = useAuth();

    const clearFields = () => {
        setSelected('');
        setCustomValue('');
        setAmount(0);
        setDescription('');
    };

    const handleSubmit = async () => {
        const category = isCustom ? customValue : selected;

        if (!category || !amount || !description) {
            alert('All fields are required.');
            return;
        }

        const expense = {
            amount: Number(amount),
            category,
            description,
        };

        try {
            const exp = await axios.post(
                'http://127.0.0.1:8000/api/expense/create_expense',
                expense,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            getExpenses();
            console.log(exp);
            clearFields();
        } catch (err) {
            console.error('Error creating expense:', err);
        }
    };

    return (

        <table className="create-expense-table">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Description</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td data-label="Category">
                        {!isCustom ? (
                            <select value={selected} onChange={e => setSelected(e.target.value)}>
                                <option value="">Select Category</option>
                                {categories.map(cat => (
                                    <option key={cat} value={cat}>
                                        {cat}
                                    </option>
                                ))}
                                <option value="Custom">Custom</option>
                            </select>
                        ) : (
                            <input
                                type="text"
                                placeholder="Enter custom category"
                                value={customValue}
                                onChange={e => setCustomValue(e.target.value)}
                            />
                        )}
                    </td>
                    <td data-label="Amount">
                        <input
                            type="number"
                            value={amount}
                            placeholder="Amount"
                            onChange={e => setAmount(e.target.value === '' ? '' : parseFloat(e.target.value))}
                        />
                    </td>
                    <td data-label="Description">
                        <input
                            type="text"
                            value={description}
                            placeholder="Description"
                            onChange={e => setDescription(e.target.value)}
                        />
                    </td>
                    <td data-label="Action">
                        <button onClick={clearFields}>Cancel</button>
                        <button onClick={handleSubmit}>Submit</button>
                    </td>
                </tr>
            </tbody>
        </table>

    );
}

export default CreateExpense;
