#include <std_lib_facilities.h>

// Символ камней:
constexpr char symb = '*';

// Заголовок игры:
const string heading = "\t \t ИГРА НИМ \nВы можете взять любое число фишек из любого ряда. \nВыигрывает тот, кто возьмет последнюю фишку.\n";

// Начальные камни:
vector<int> start_rocks = {3, 4, 5};

// Инструкция для ходов:
const string directions = "Введите ваш ход в формате РЯД КОЛИЧ (например, 2 3 - взять из 2 ряда 3 фишки)\nВведите 0 0 для выхода из игры \n";

// Создание ряда камней
string make_row(char symb, int len)
{
    string ans = "";
    while (len > 0)
    {
        ans += symb;
        len -= 1;
    }
    return ans;
}

// Вывод экрана меню
void menu(string heading, vector<int> rocks, string directions)
{
    cout << "\n"
         << heading
         << "\n";
    cout << "   Номер ряда \t \t  Кол-во фишек\n";
    for (size_t i = 0; i < rocks.size(); ++i)
    {
        cout << "\t" << i + 1 << "\t " << make_row(symb, rocks[i]) << "\t \t" << rocks[i] << "\n";
    }
    cout << "\n"
         << directions;
}

// Ход игрока(возвращает измененное поле)
vector<int> player_turn(int number, vector<int> rocks)
{
    switch (number)
    {
    case -1:
        cout << "\nХОД ИГРОКА";
        break;

    default:
        cout << "\nХОД " << number << " ИГРОКА";
        break;
    }
    menu(" ", rocks, directions);
    int row, amount;
    bool correct_values = false;

    if (cin)
    {
        while (!correct_values)
        {
            cin >> row;
            cin >> amount;
            if (row == 0 or amount == 0)
            {
                exit(0);
            }
            else if (row < 0 or amount < 0)
            {
                cout << "Неверное значение!\n";
            }
            else if (row <= rocks.size())
            {
                if (amount <= rocks[row - 1])
                {
                    correct_values = true;
                    rocks[row - 1] -= amount;
                }
                else
                {
                    cout << "Неверное значение!\n";
                }
            }
            else
            {
                cout << "Неверное значение!\n";
            }
        }
        return rocks;
    }
    else
    {
        throw runtime_error("Некорректный ход");
    }
}

// Сумма камней
int rocks_sum(vector<int> rocks)
{
    int sum = 0;
    for (int i = 0; i < rocks.size(); ++i)
    {
        sum += rocks[i];
    }
    return sum;
}

int bin_rocks_sum(vector<int> rocks)
{
    int sum = 0;
    for (int i = 0; i < rocks.size(); ++i)
    {
        sum ^= rocks[i];
    }
    return sum;
}

// Рандомный ход
vector<int> random_turn(vector<int> rocks)
{
    for (int i = 0; i < rocks.size(); ++i)
    {
        if (rocks[i] > 0)
        {
            rocks[i] -= 1;
            break;
        }
    }
    return rocks;
}

// Ход компьютера
vector<int> computer_turn(int number, vector<int> rocks)
{
    cout << "\nХОД КОМПЬЮТЕРА \n"; ///////////// ТАЙМЕР
    menu(" ", rocks, directions);

    if (bin_rocks_sum(rocks) == 0)
    {
        rocks = random_turn(rocks);
    }
    else
    {
        for (int i = 0; i < rocks.size(); ++i)
        {
            if ((bin_rocks_sum(rocks) ^ rocks[i]) < rocks[i])
            {
                rocks[i] = bin_rocks_sum(rocks) ^ rocks[i];
                break;
            }
        }
    }

    return rocks;
}

// Режим игры с компьютером
void one_player(vector<int> rocks)
{
    cout << "\nВы вошли в режим игры для одного игрока \n";
    bool game_end = false;
    int turn_num = -1; //-1 - ход игрока
                       // 0  - ход компьютера
    while (!game_end)
    {
        if (rocks_sum(rocks) != 0)
        {
            switch (turn_num)
            {
            case -1:
                rocks = player_turn(turn_num, rocks);
                break;

            case 0:
                rocks = computer_turn(turn_num, rocks);
                break;
            }

            if (turn_num == 0)
            {
                turn_num = -1;
            }
            else
            {
                turn_num = 0;
            }
        }
        else
        {
            cout << "ПОБЕДА " << ((turn_num == -1) ? "КОМПЬЮТЕРА" : "ИГРОКА")
                 << "\n";
            game_end = true;
        }
    }
}

// Режим игры с 2 игроками
void two_players(vector<int> rocks)
{
    cout << "\nВы вошли в режим игры для двоих игроков \n";
    bool game_end = false;
    int turn_num = 1;
    while (!game_end)
    {
        if (rocks_sum(rocks) != 0)
        {
            rocks = player_turn(turn_num, rocks);
            if (turn_num == 1)
            {
                turn_num = 2;
            }
            else
            {
                turn_num = 1;
            }
        }
        else
        {
            cout << "ПОБЕДА " << ((turn_num == 1) ? "2" : "1") << " ИГРОКА"
                 << "\n";
            game_end = true;
        }
    }
}

// Выбор режима игры (1/2 игрока)
void choose_game(vector<int> rocks)
{
    // menu(heading, rocks, "");
    cout << "Введите 1, чтобы включить одиночный режим игры\n"
         << "Введите 2, чтобы включить режим игры для двоих\n";
    int set = 0;

    cin >> set;
    bool correct_value = false;

    if (cin)
    {
        while (!correct_value)
        {
            if (set == 1)
            {
                one_player(rocks);
                correct_value = true;
            }
            else
            {
                if (set == 2)
                {
                    two_players(rocks);
                    correct_value = true;
                }
                else
                {
                    cout << "Неверное значение!\n";
                    cin >> set;
                }
            }
        }
    }
    else
    {
        throw runtime_error("Некорректный ввод режима игры");
    }
}

int main()
{
    try
    {
        bool game_running = true;
        // choose_game();

        while (game_running)
        {
            vector<int> rocks = start_rocks;
            choose_game(rocks);
            // menu(heading, rocks, directions);
        }
        return 0;
    }

    catch (runtime_error &e)
    {
        cerr << "Ошибка: " << e.what() << "\n";
        keep_window_open();
        return 1;
    }
}