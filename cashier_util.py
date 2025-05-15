import math

stock = {1: 200, 2: 200, 5: 200, 10: 200, 20: 200, 50: 20, 100: 10, 200: 10, 500: 10}
currencies = list(stock.keys())
currencies.sort(reverse=True)

# total_cash = list(map(lambda x: x[0]*x[1], stock.items()))
total_cash = sum([k * v for k, v in stock.items()])
transaction_counter = 0
print("=" * 50)
print(f"You have total Cash of Rs [{total_cash}]")
print(stock)
print("=" * 50)


def make_transaction(amount):
    if amount > total_cash:
        print("Insufficient Cash in Cashier")
        return

    cash = []
    for k, v in stock.items():
        if amount >= k:
            count = amount // k
            if count > v:
                count = v
            cash.append((k, count))
            amount -= k * count
            stock[k] -= count

    if amount == 0:
        print("Transaction Successful")
        print(cash)
    else:
        print("Transaction Failed")
        print("Cash returned: ", amount)


def receive_payment(payment_amount: int, denomination: dict):
    global total_cash, transaction_counter
    total_received_amount = sum([k * v for k, v in denomination.items()])
    transaction_counter += 1

    print("*" * 20 + " TRANSACTION [" + str(transaction_counter) + "] " + "*" * 20)
    print(f"Incoming Transaction of Rs: [{payment_amount}]. User has given [{total_received_amount}]")

    if total_received_amount < payment_amount:
        print("Insufficient Payment")
        print("x" * 50)
        return None
    else:
        return_amount = total_received_amount - payment_amount
        print(f"Return Amount: {return_amount}")

        can_transact = False

        return_pile = {}

        for i in range(0, len(currencies)):
            note = currencies[i]
            note_quantity = stock[currencies[i]]
            if return_amount >= note:
                count = math.floor(return_amount / note)
                if note_quantity >= count:
                    # stock[note] -= count
                    return_pile[note] = count
                    return_amount -= note * count
                elif note_quantity > 0:
                    # stock[note] -= note_quantity
                    return_pile[note] = note_quantity
                    return_amount -= note * (note_quantity)
                if return_amount == 0:
                    can_transact = True
                    break

        # add stock currency
        for k, v in denomination.items():
            stock[k] += v
        total_cash += payment_amount

        # remove returned currency
        if can_transact:
            for k, v in return_pile.items():
                stock[k] -= v
                # total_cash -= k * v
        else:
            print("We do not have sufficient change to return.")
            print("x"*50)
            return None

        print("Return Pile: ", return_pile)
        print(f"Updated stock amount Rs: [{total_cash}]")
        print(stock)
        print("-" * 50)
        return return_pile


receive_payment(125, {500: 1})
receive_payment(123, {500: 1})
receive_payment(122, {500: 1})
receive_payment(121, {500: 1})
receive_payment(120, {500: 1})
receive_payment(119, {500: 1})
receive_payment(118, {500: 1})
receive_payment(117, {500: 1})
receive_payment(116, {500: 1})
receive_payment(115, {500: 1})
receive_payment(114, {500: 1})
receive_payment(113, {500: 1})
receive_payment(112, {500: 1})
receive_payment(111, {500: 1})
receive_payment(109, {500: 1})
receive_payment(108, {500: 1})
receive_payment(107, {500: 1})
receive_payment(106, {500: 1})
receive_payment(105, {500: 1})
receive_payment(104, {500: 1})
receive_payment(103, {500: 1})
receive_payment(102, {500: 1})
receive_payment(101, {500: 1})
receive_payment(100, {500: 1})
receive_payment(99, {500: 1})
receive_payment(98, {500: 1})
receive_payment(97, {500: 1})
receive_payment(96, {500: 1})
receive_payment(95, {500: 1})
receive_payment(94, {500: 1})
receive_payment(93, {200: 1})
receive_payment(92, {200: 1})
receive_payment(91, {50: 2})
receive_payment(90, {200: 1})


