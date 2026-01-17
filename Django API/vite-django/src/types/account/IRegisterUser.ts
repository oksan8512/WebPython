import type {UploadFile} from "antd";
import type {RcFile} from "antd/es/upload";

export interface IRegisterUser {
    email: string;
    username:string;
    password: string;
    confirmPassword: string;
    phone: string;
    first_name: string;
    last_name: string;
    image: RcFile | null | Array<UploadFile>; // RcFile - це тип файлу в antd
}