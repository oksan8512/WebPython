import {Button, Form, Input, Upload} from "antd";
import { InboxOutlined } from '@ant-design/icons';
import type {IRegisterUser} from "../types/account/IRegisterUser.ts";
import axios from "axios";

const RegisterPage = () => {
    const [form] = Form.useForm<IRegisterUser>();

    const onFinish = (values: IRegisterUser) => {
        // if(values.image?.type == UploadFile)
        if (Array.isArray(values.image)) {
            values.image = values.image[0].originFileObj!;
            // console.log("Is array", values.image[0]);
        }
        axios.post("http://localhost:4099/api/users/register/", values,
            {
                headers: {'Content-Type': 'multipart/form-data'}
            })
            .then(res => {
                console.log("Register is good", res);
            });
        console.log('Success:', values);
    }

    const normFile = (e: any) => {
        console.log('Upload event:', e);
        if (Array.isArray(e)) {
            // console.log('Upload event length:', e.length);
            return e;
        }
        const n = e?.fileList.length;
        // console.log('Upload event file select:', e?.file);
        // form.setFieldValue("image", e?.File);
        // console.log("image value", form.getFieldValue("image"));
        // return e?.fileList;
        if(n<1) return e?.fileList;
        return [e?.fileList[n-1]];
        //return e?.fileList;
    };

    return (
        <div className={"min-h-screen xl:flex"}>
            <div className="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6">
                <h1 className="mb-4 text-center text-4xl font-bold tracking-tight text-heading md:text-5xl lg:text-6xl">
                    Реєстрація користувача
                </h1>

                <div className="overflow-hidden rounded-2xl
                    border border-gray-200 bg-white px-4 pb-3 pt-4
                    dark:border-gray-800 dark:bg-white/[0.03] sm:px-6">

                    <div className="max-w-full overflow-x-auto">
                        <Form onFinish={onFinish}
                            // className={"w-full"}
                              form={form}
                              layout={"vertical"}
                        >
                            <Form.Item<IRegisterUser>
                                label={"Електронна пошта"}
                                name={"email"}
                                rules={[{ required: true, message: 'Вкажіть пошту'}]}
                            >
                                <Input/>
                            </Form.Item>

                            <Form.Item<IRegisterUser>
                                label={"Логін користувача"}
                                name={"username"}
                                rules={[{ required: true, message: 'Вкажіть логін'}]}
                            >
                                <Input/>
                            </Form.Item>

                            <Form.Item<IRegisterUser>
                                label={"Прізвище"}
                                name={"first_name"}
                                rules={[{ required: true, message: 'Вкажіть прізвище'}]}
                            >
                                <Input/>
                            </Form.Item>

                            <Form.Item<IRegisterUser>
                                label={"Ім'я"}
                                name={"last_name"}
                                rules={[{ required: true, message: "Вкажіть ім'я"}]}
                            >
                                <Input/>
                            </Form.Item>

                            <Form.Item<IRegisterUser>
                                label={"Телефон"}
                                name={"phone"}
                                rules={[{
                                    required: true,
                                    message: "Вкажіть телефон"
                                }, {max: 15}, {
                                    pattern: /^[\\+]?[(]?[0-9]{3}[)]?[-\\s\\.]?[0-9]{3}[-\\s\\.]?[0-9]{4,6}$/,
                                    message: "Вкажіть валідний номер телефона!"
                                }]}
                            >
                                <Input/>
                            </Form.Item>

                            <Form.Item<IRegisterUser>
                                label={"Пароль"}
                                name={"password"}
                                rules={[{
                                    required: true,
                                    message: "Вкажіть пароль"
                                },
                                    {max: 20, message:"Пароль не може містити більше 20 символів"},
                                    {
                                        pattern: /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/,
                                        message: "Пароль має містити 1 велику, 1 маленьку букву, 1 цифру і 1 спеціальний символ"
                                    }]}
                            >
                                <Input.Password/>
                            </Form.Item>

                            <Form.Item<IRegisterUser>
                                label={"Підтвердження паролю"}
                                name={"confirmPassword"}
                                rules={[
                                    {required: true, message: "Вкажіть підтвердження пароль"},
                                    ({ getFieldValue }) => ({
                                        validator(_, value) {
                                            if (!value || getFieldValue('password') === value) {
                                                return Promise.resolve();
                                            }
                                            return Promise.reject(new Error('Паролі не збігаються!'));
                                        },
                                    }),
                                    {max:20, message:"Пароль не може містити більше ніж 20 символів"}
                                ]}
                            >
                                <Input.Password/>
                            </Form.Item>

                            <Form.Item label="Dragger">
                                <Form.Item<IRegisterUser> name="image" valuePropName="fileList"
                                                          getValueFromEvent={normFile}
                                                          noStyle>
                                    <Upload.Dragger name="files" multiple={false}
                                                    listType="picture"
                                                    accept={"image/*"}
                                                    beforeUpload={() => {return false;}}
                                    >
                                        <p className="ant-upload-drag-icon">
                                            <InboxOutlined />
                                        </p>
                                        <p className="ant-upload-text">Click or drag file to this area to upload</p>
                                        <p className="ant-upload-hint">Support for a single or bulk upload.</p>
                                    </Upload.Dragger>
                                </Form.Item>
                            </Form.Item>

                            <Form.Item label={null}>
                                <Button type="primary" htmlType="submit">
                                    Реєстрація
                                </Button>
                            </Form.Item>

                        </Form>
                    </div>
                </div>


            </div>
        </div>
    );
}

export default RegisterPage;