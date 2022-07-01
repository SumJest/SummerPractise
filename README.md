##  Распознователь цепочки
### Описание
Алгоритм распознаёт цепочку для языка программирования Pascal, заданную с помощью формул Бэкуса-Наура.
```
<цепочка>::=<описание константы>
	<описание константы>::=CONST <идентификатор>=<значение>;
		<идентификатор>::=<буква>|<идентификатор><буква>|<идентификатор><цифра>
			<буква>::=A | B | C | D | E | F | ... | Z
			<цифра>::=0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
		<значение>::=<целая константа> | <16-ричная константа>
			<целая константа>::=<целое со знаком> | <целое без знака>
				<целое без знака>::=<цифра> | <цифра><целое без знака>
				<целое со знаком>::=<знак><целое без знака>
						<знак>::=+ | -
		<16-ричная константа>::= $<список 16-ричных букв и цифр>
			<список 16-ричных букв и цифр>::=<цифра> | <16-ричная буква><список 16-ричных букв и цифр>
				<16-ричная буква>::=A | B | C | D | E | F
```
Помимо этого, на цепочку накладывается следующее семантическое ограничение: идентификатор, входящий в цепочку, не должен совпадать с ключевыми словами языка Pascal.

**Описание входных данных.**<br />
Цепочка записана в текстовом файле INPUT.TXT, который состоит из одной строки. Длина цепочки не превышает 80 символов. <br />
**Описание выходных данных.**<br />
Результат распознавания необходимо записать в текстовый файл OUTPUT.TXT в одно из следующих сообщений: ACCEPT, если цепочка допустима, и REJECT, если цепочка недопустима, пример данных представлен в таблице 1.

|      INPUT.TXT             |      OUTPUT.TXT     |
|----------------------------|---------------------|
|     const one=1;           |     ACCEPT          |
|     const Code=-23;        |     ACCEPT          |
|     const HEX=$10A1;       |     ACCEPT          |
|     const   a1b3=-13;      |     ACCEPT          |
|     const   abc1=$1;       |     ACCEPT          |
|     const   1abc=13;       |     REJECT          |
|     const   abc=+-8;       |     REJECT          |
|     const   variable=13    |     REJECT          |
|     const   varr=9$1;      |     REJECT          |
|     const   varrr=$1A;     |     REJECT          |

### Структура
[![Структура](https://imgur.com/iCrPuz1.jpg "Структура")](https://imgur.com/iCrPuz1 "Структура")

1. [Программа](https://github.com/SumJest/SummerPractise/blob/master/main.py "Программа")
2. [Блок транслитерации](https://github.com/SumJest/SummerPractise/blob/master/blocks/translator.py " Блок транслитерации")
3. [Лексический блок](https://github.com/SumJest/SummerPractise/blob/master/blocks/lexical.py "Лексический блок")
4. [Синтаксический блок](https://github.com/SumJest/SummerPractise/blob/master/blocks/syntax.py "Синтаксический блок")
5. [Блок журнала](https://github.com/SumJest/SummerPractise/blob/master/blocks/logging.py "Блок журнала")
6. [Блок работы с файлами](https://github.com/SumJest/SummerPractise/blob/master/blocks/filemanager.py "Блок работы с файлами")

#### Программа
Основной файл управляет всеми остальными блоками, конкретней функция [`check`](https://github.com/SumJest/SummerPractise/blob/master/main.py#L10 "`check`"). Ввод и вывод данных осуществляется через файлы **input.txt** и **output.txt** соответственно. Они находятся в корне проекта.
#### Блок транслитерации
Блок представлен классом **Translator**. Трансляция осуществляется через функцию [translate](https://github.com/SumJest/SummerPractise/blob/master/blocks/translator.py#L54 "translate"). На вход принимается строка, на выходе список кортежей, состоящих из символа и его [SymbolClass](https://github.com/SumJest/SummerPractise/blob/master/blocks/translator.py#L10 "SymbolClass").

Блок осуществляет проверку всех представленных в цепочке символов на верность описанию. А так же присваивает им один из классов:
- letter ("a-zA-Z")
- digit ("0-9")
- sign ("+-")
- equal ("=")
- dollar ("$")
- semicolon (";")
- space (" ")

Пример вывода блока транслитерации при вводной строке `const a=$1;`:

| str | Symbol Class |
|-----|--------------|
| c   | letter       |
| o   | letter       |
| n   | letter       |
| s   | letter       |
| t   | letter       |
|     | space        |
| a   | letter       |
| =   | equal        |
| $   | dollar       |
| 1   | digit        |
| ;   | semicolon    |

Блок бросает исключение `TranslatorError`, когда встречает непредусмотренный символ.

#### Лексический блок

Блок представлен классом **Lexical**. Трансляция осуществляется через функцию [lexical_analyze](https://github.com/SumJest/SummerPractise/blob/master/blocks/lexical.py#L149 "lexical_analyze"). На вход принимается выходные данные транслятора, на выходе список кортежей, состоящих из строки и [WordClass](https://github.com/SumJest/SummerPractise/blob/master/blocks/lexical.py#L23 "WordClass").

Блок идентифицирует десятичные и шестнадцатиричные числа, идентификаторы и служебные слова. В случае не соответствия выбрасывает исключение `LexicalError`.

Все классы:
- identifier
- number
- hex_number
- equal
- semicolon
- space
- service_name

Пример выходных данных лексического блока при вышеперечисленных выходных: 

| str   | Word Class   |
|-------|--------------|
| const | service_name |
|       | space        |
| a     | identifier   |
| =     | equal        |
| $1    | hex_number   |
| ;     | semicolon    |

Работа блока основана на следующем конечном автомате:

|                     | letter              | digit              | sign   | equal | dollar             | semicolon | space |     |
|---------------------|---------------------|--------------------|--------|-------|--------------------|-----------|-------|-----|
| idle                | identifier          | number             | number | idle  | hex\_number\_digit | idle      | idle  | 1   |
| identifier          | identifier          | identifier         | E      | idle  | E                  | idle      | idle  | 0   |
| number              | E                   | number             | E      | idle  | E                  | idle      | idle  | 0   |
| hex\_number\_letter | hex\_number\_letter | hex\_number\_digit | E      | E     | E                  | E         | E     | 0   |
| hex\_number\_digit  | hex\_number\_letter | hex\_number\_digit | E      | idle  | E                  | idle      | idle  | 0   |
| E                   | E                   | E                  | E      | E     | E                  | E         | E     | 0   |

#### Синтаксический блок

Блок представлен классом **Syntax**. Трансляция осуществляется через функцию [syntax_analyze](https://github.com/SumJest/SummerPractise/blob/master/blocks/syntax.py#L72 "syntax_analyze"). На вход принимается выходные данные лексического блока, на выходе строка **ACCEPT** в случае соответствие цепочки формулам. В ином случае блок выбрасывает исключение `SyntaxBlockError`.

Работа блок основана на следующем конечном автомате:

|                        | identifier | number | hex\_number | equal | semicolon | space | service\_name          |     |
|------------------------|------------|--------|-------------|-------|-----------|-------|------------------------|-----|
| start                  | E          | E      | E           | E     | E         | E     | service\_name\_const | 0   |
| service\_name\_const | E          | E      | E           | E     | E         | space | E                      | 0   |
| space                  | identifier | E      | E           | E     | E         | space | E                      | 0   |
| identifier             | E          | E      | E           | equal | E         | E     | E                      | 0   |
| equal                  | E          | value  | value       | E     | E         | E     | E                      | 0   |
| value                  | E          | E      | E           | E     | semicolon | E     | E                      | 0   |
| semicolon              | E          | E      | E           | E     | E         | E     | E                      | 1   |
| E                      | E          | E      | E           | E     | E         | E     | E                      | 0   |

#### Блок журнала

В блоке находится функция [log](https://github.com/SumJest/SummerPractise/blob/master/blocks/logging.py#L27 "log"). 
На вход принимаются строка сообщения и [LogStatus](https://github.com/SumJest/SummerPractise/blob/master/blocks/logging.py#L8 "LogStatus").
Статусы:
- INFO
- WARN
- ERROR

Функция получает название файла, из которого она вызвана это является именем блока. Формирует сообщение по образцу: `"[{status}] [{time}] {blockname}: {msg}"`. И отправляет вместе с именем блока в блок работы с файлами, чтобы тот записал его в соответсвующий log файл, а также отправляет такое же сообщение в консоль.

К функции **log** имеет доступ любой блок.

#### Блок работы с файлами
Блок представлен классом **FileManager**.
В этом классе есть три основных функции:
- [input](https://github.com/SumJest/SummerPractise/blob/master/blocks/filemanager.py#L25 "input") - Берет данный из входного файла
- [output](https://github.com/SumJest/SummerPractise/blob/master/blocks/filemanager.py#L36 "output") - Записывает данные в выходной файл
- [write_log](https://github.com/SumJest/SummerPractise/blob/master/blocks/filemanager.py#L45 "write_log") - Записывает сообщение в журнал блока.